// You can edit this code!
// Click here and start typing.
package main

import (
	"fmt"
	"strings"
)

func main() {

	var parameter_keys []string
	fmt.Println("Hello, 世界")
	value := "arn:aws:ssm:us-east-1:824238433314:par"
	fmt.Println(value)
	res1 := strings.Split(value, "parameter")
	fmt.Println(res1)
	//parameter_keys = append(parameter_keys, res1[1])
	if len(res1) == 2 {
		parameter_keys = append(parameter_keys, res1[1])
	}
	fmt.Println(parameter_keys)
}
