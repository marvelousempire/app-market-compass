// Language Pie EMA comparison: same finite f64 input and periods as Pandas.
package main
import (
 "encoding/binary"
 "encoding/json"
 "fmt"
 "math"
 "os"
 "strconv"
 "strings"
 "time"
)
type Result struct {
 Engine string `json:"engine"`
 Count int `json:"count"`
 Rounds int `json:"rounds"`
 ComputeMs float64 `json:"compute_ms"`
 Last map[string]float64 `json:"last"`
 Checksum map[string]float64 `json:"checksum"`
}
func ema(prices []float64, period int) []float64 {
 out:=make([]float64,len(prices))
 for i:=range out {out[i]=math.NaN()}
 if len(prices)==0 {return out}
 alpha:=2.0/float64(period+1)
 value:=prices[0]
 if period==1 {out[0]=value}
 for i:=1;i<len(prices);i++ {
   value=(1-alpha)*value+alpha*prices[i]
   if i>=period-1 {out[i]=value}
 }
 return out
}
func checksum(a []float64, period int) float64 {
 sum:=0.0
 for i:=period-1;i<len(a);i+=19 {sum+=a[i]}
 return sum
}
func fail(s string) {fmt.Fprintln(os.Stderr,s);os.Exit(2)}
func main() {
 if len(os.Args)!=4 {fail("usage: ema-go INPUT-f64le.bin ROUNDS PERIODS-comma-separated")}
 rounds,err:=strconv.Atoi(os.Args[2]);if err!=nil||rounds<1||rounds>100000 {fail("invalid rounds")}
 bytes,err:=os.ReadFile(os.Args[1]);if err!=nil {fail(err.Error())}
 if len(bytes)==0||len(bytes)%8!=0 {fail("invalid input: expected little-endian float64 array")}
 prices:=make([]float64,len(bytes)/8)
 for i:=range prices {
   prices[i]=math.Float64frombits(binary.LittleEndian.Uint64(bytes[i*8:]))
   if math.IsNaN(prices[i])||math.IsInf(prices[i],0) {fail("nonfinite price")}
 }
 periods:=[]int{}
 for _,part:=range strings.Split(os.Args[3],",") {
   p,e:=strconv.Atoi(part)
   if e!=nil||p<1||p>len(prices) {fail("invalid period: "+part)}
   periods=append(periods,p)
 }
 if len(periods)==0 {fail("no periods")}
 for _,p:=range periods {_=checksum(ema(prices,p),p)}
 result:=Result{Engine:"go",Count:len(prices),Rounds:rounds,Last:map[string]float64{},Checksum:map[string]float64{}}
 start:=time.Now()
 for r:=0;r<rounds;r++ {
   for _,p:=range periods {
     out:=ema(prices,p)
     result.Last[strconv.Itoa(p)]=out[len(out)-1]
     result.Checksum[strconv.Itoa(p)]=checksum(out,p)
   }
 }
 result.ComputeMs=float64(time.Since(start).Microseconds())/1000
 if e:=json.NewEncoder(os.Stdout).Encode(result);e!=nil {fail(e.Error())}
}
