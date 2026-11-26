//! Deterministic research calculations for Market Compass.
//! Slice 1: European-style option scenarios, compiled for native tests and WebAssembly.

const RATE: f64 = 0.04;

#[no_mangle]
pub extern "C" fn market_compass_engine_abi() -> i32 { 2 }

fn normal_cdf(x: f64) -> f64 {
    let a = x.abs();
    let t = 1.0 / (1.0 + 0.231_641_9 * a);
    let pdf = (-a * a / 2.0).exp() / (2.0 * std::f64::consts::PI).sqrt();
    let c = 1.0 - pdf * (0.319_381_530 * t - 0.356_563_782 * t.powi(2)
        + 1.781_477_937 * t.powi(3) - 1.821_255_978 * t.powi(4)
        + 1.330_274_429 * t.powi(5));
    if x < 0.0 { 1.0 - c } else { c }
}

/// European-style Black-Scholes value. `kind`: 0 call, 1 put.
/// Inputs outside the declared domain produce NaN, so a receiving UI can refuse.
#[no_mangle]
pub extern "C" fn option_price(spot: f64, strike: f64, days: f64, iv_percent: f64, kind: i32) -> f64 {
    if !spot.is_finite() || !strike.is_finite() || !days.is_finite() || !iv_percent.is_finite()
        || spot < 0.0 || (spot == 0.0 && days > 0.0) || strike <= 0.0 || days < 0.0 || iv_percent <= 0.0
        || (kind != 0 && kind != 1)
    {
        return f64::NAN;
    }
    if days == 0.0 {
        return if kind == 0 { (spot - strike).max(0.0) } else { (strike - spot).max(0.0) };
    }
    let t = days / 365.0;
    let vol = iv_percent / 100.0;
    let root = t.sqrt();
    let d1 = ((spot / strike).ln() + (RATE + vol * vol / 2.0) * t) / (vol * root);
    let d2 = d1 - vol * root;
    if kind == 0 {
        spot * normal_cdf(d1) - strike * (-RATE * t).exp() * normal_cdf(d2)
    } else {
        strike * (-RATE * t).exp() * normal_cdf(-d2) - spot * normal_cdf(-d1)
    }
}

#[no_mangle]
pub extern "C" fn option_quote(spot: f64, strike: f64, days: f64, iv_percent: f64, kind: i32) -> f64 {
    let value = option_price(spot, strike, days, iv_percent, kind);
    if value.is_finite() {
        let rounded = (value * 100.0).round() / 100.0;
        if days > 0.0 { rounded.max(0.01) } else { rounded }
    } else { f64::NAN }
}

#[no_mangle]
pub extern "C" fn option_return(
    current_spot: f64, projected_spot: f64, strike: f64, current_days: f64,
    projected_days: f64, current_iv: f64, projected_iv: f64, kind: i32,
    side: i32, quantity: i32,
) -> f64 {
    if (side != 1 && side != -1) || !(1..=100).contains(&quantity)
        || projected_days > current_days
    { return f64::NAN; }
    let entry = option_quote(current_spot, strike, current_days, current_iv, kind);
    let exit = option_quote(projected_spot, strike, projected_days, projected_iv, kind);
    (exit - entry) * 100.0 * f64::from(quantity) * f64::from(side)
}

/// Return for a same-expiration, two-leg hypothetical strategy. Each side is
/// +1 for long or -1 for short. Quotes remain illustrative, not market fills.
#[no_mangle]
pub extern "C" fn option_two_leg_return(
    current_spot: f64, projected_spot: f64, current_days: f64, projected_days: f64,
    current_iv: f64, projected_iv: f64,
    strike_a: f64, kind_a: i32, side_a: i32,
    strike_b: f64, kind_b: i32, side_b: i32, quantity: i32,
) -> f64 {
    let a = option_return(current_spot, projected_spot, strike_a, current_days,
        projected_days, current_iv, projected_iv, kind_a, side_a, quantity);
    let b = option_return(current_spot, projected_spot, strike_b, current_days,
        projected_days, current_iv, projected_iv, kind_b, side_b, quantity);
    if a.is_finite() && b.is_finite() { a + b } else { f64::NAN }
}

#[no_mangle]
pub extern "C" fn option_two_leg_entry(
    spot: f64, days: f64, iv: f64,
    strike_a: f64, kind_a: i32, side_a: i32,
    strike_b: f64, kind_b: i32, side_b: i32,
) -> f64 {
    if (side_a != 1 && side_a != -1) || (side_b != 1 && side_b != -1) {
        return f64::NAN;
    }
    let a = option_quote(spot, strike_a, days, iv, kind_a);
    let b = option_quote(spot, strike_b, days, iv, kind_b);
    if a.is_finite() && b.is_finite() { a * f64::from(side_a) + b * f64::from(side_b) } else { f64::NAN }
}


#[no_mangle]
pub extern "C" fn option_delta(spot: f64, strike: f64, days: f64, iv_percent: f64, kind: i32) -> f64 {
    (option_price(spot + 0.01, strike, days, iv_percent, kind)
        - option_price(spot - 0.01, strike, days, iv_percent, kind)) / 0.02
}

#[no_mangle]
pub extern "C" fn option_theta_day(spot: f64, strike: f64, days: f64, iv_percent: f64, kind: i32) -> f64 {
    option_price(spot, strike, (days - 1.0).max(0.0), iv_percent, kind)
        - option_price(spot, strike, days, iv_percent, kind)
}

#[no_mangle]
pub extern "C" fn option_vega_point(spot: f64, strike: f64, days: f64, iv_percent: f64, kind: i32) -> f64 {
    option_price(spot, strike, days, iv_percent + 1.0, kind)
        - option_price(spot, strike, days, iv_percent, kind)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn call_put_parity_and_expiry() {
        let c = option_price(100.0, 100.0, 30.0, 25.0, 0);
        let p = option_price(100.0, 100.0, 30.0, 25.0, 1);
        let parity = 100.0 - 100.0 * (-RATE * 30.0 / 365.0).exp();
        assert!((c - p - parity).abs() < 0.001);
        assert_eq!(option_price(120.0, 100.0, 0.0, 25.0, 0), 20.0);
        assert_eq!(option_price(120.0, 100.0, 0.0, 25.0, 1), 0.0);
        assert_eq!(option_price(0.0, 100.0, 0.0, 25.0, 1), 100.0);
        assert!(option_price(0.0, 100.0, 1.0, 25.0, 1).is_nan());
    }
    #[test]
    fn baseline_zero_and_sensitivity() {
        let baseline = option_return(230.0, 230.0, 230.0, 9.0, 9.0, 30.0, 30.0, 0, 1, 1);
        assert_eq!(baseline, 0.0);
        assert!(option_return(230.0, 250.0, 230.0, 9.0, 9.0, 30.0, 30.0, 0, 1, 1) > 0.0);
        assert!(option_return(230.0, 230.0, 230.0, 9.0, 0.0, 30.0, 30.0, 0, 1, 1) < 0.0);
        assert!(option_return(230.0, 230.0, 230.0, 9.0, 9.0, 30.0, 45.0, 0, 1, 1) > 0.0);
    }
    #[test]
    fn refuses_invalid_inputs() {
        assert!(option_price(-1.0, 100.0, 30.0, 20.0, 0).is_nan());
        assert!(option_price(100.0, 100.0, 30.0, 20.0, 2).is_nan());
        assert!(option_return(100.0, 100.0, 100.0, 30.0, 31.0, 20.0, 20.0, 0, 1, 1).is_nan());
    }
    #[test]
    fn two_leg_spread_and_straddle() {
        let spread = option_two_leg_return(100.0, 120.0, 30.0, 0.0, 25.0, 25.0,
            100.0, 0, 1, 110.0, 0, -1, 1);
        assert!(spread > 0.0);
        let baseline = option_two_leg_return(100.0, 100.0, 30.0, 30.0, 25.0, 25.0,
            100.0, 0, 1, 110.0, 0, -1, 1);
        assert_eq!(baseline, 0.0);
        let straddle = option_two_leg_return(100.0, 125.0, 30.0, 0.0, 25.0, 25.0,
            100.0, 0, 1, 100.0, 1, 1, 1);
        assert!(straddle > 0.0);
        assert!(option_two_leg_return(100.0, 100.0, 30.0, 31.0, 25.0, 25.0,
            100.0, 0, 1, 100.0, 1, 1, 1).is_nan());
    }
}
