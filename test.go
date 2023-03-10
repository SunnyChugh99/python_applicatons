package main

import (
	// "encoding/base64"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"io/ioutil"
	"strings"
	"encoding/json"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/arn"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/ssm"
	"github.com/hashicorp/vault/api"
)

func main() {
	secretArn := os.Getenv("SECRET_ARN")
	secretFilename := os.Getenv("SECRET_FILENAME")
	injectorType := os.Getenv("INJECTOR_TYPE")

    secretArn = arn:aws:ssm:us-east-1:824238433314:parameteradmin1234
    secretFilename = mosaic-secret-manager.ini // /tmp/mosaic-automl-backend.ini
	injectorType = SSM,hvs.CAESIHSHgj-GdZwaYufvjMw6tRBkrt33LXgkPqlqVzgR-GqMGh4KHGh2cy5LOURhcEUwT0trWGQ5aFE1SXFJb2JFY3E,secret/mosaic-ai/config,http://release...





	fmt.Println(injectorType)
	var AWSRegion string
	s := strings.Split(injectorType, ",")

	s = [SSM,hvs.CAESIHSHgj-GdZwaYufvjMw6tRBkrt33LXgkPqlqVzgR-GqMGh4KHGh2cy5LOURhcEUwT0trWGQ5aFE1SXFJb2JFY3E,secret/mosaic-ai/config,http://release...]
	s[0] = SSM
	s[1] = vault_token
	s[2] = secret/mosaic-ai/config
	s[3] = http://release...

	list := strings.Split(secretArn,",")

	var parameter_keys []string

	for _, value := range list {
		res1 := strings.Split(value,"parameter")
		parameter_keys = append(parameter_keys,res1[1])
	}

	fmt.Println(parameter_keys)

	var result map[string]interface{}

	json.Unmarshal([]byte("{}"), &result)

	if s[0] == "SSM" {
		fmt.Println("IN SSM")
		if arn.IsARN(secretArn) {
			arnobj, _ := arn.Parse(secretArn)
			AWSRegion = arnobj.Region
		} else {
			log.Println("Not a valid ARN")
			os.Exit(1)
		}

		sess, err := session.NewSession()
		if err != nil {
			log.Panic(err)
		}
		ssmsvc := ssm.New(sess, &aws.Config{
			Region: aws.String(AWSRegion),
		})


		param, err := ssmsvc.GetParameters(&ssm.GetParametersInput{
			Names:           aws.StringSlice(parameter_keys),
			WithDecryption: aws.Bool(true),
		})

		fmt.Println(param)

		for _, value1 := range param.Parameters {
			result[*value1.Name] = *value1.Value
			fmt.Println(value1.Name)
			fmt.Println(value1.Value)
		}

		fmt.Println(result)
	}

	if s[0] == "VAULT" {
		var token = s[1]
		var vault_addr = s[3]
		fmt.Println(token)
		fmt.Println(vault_addr)
		fmt.Println("IN vault")
		config := &api.Config{
			Address: vault_addr,
		}
		client, err := api.NewClient(config)
		if err != nil {
			fmt.Println(err)
			return
		}
		client.SetToken(token)
		c := client.Logical()
		secret, err := c.Read(s[2])
		if err != nil {
			fmt.Println(err)
			return
		}

		for _, value := range parameter_keys {
			fmt.Println(value)
			fmt.Println(value[1:])
			fmt.Println(secret.Data[value[1:]])
			x := fmt.Sprint(secret.Data[value[1:]])
			result[value] = x
		}

		fmt.Println(result)

	}

	visit(result, secretFilename)

	// Decrypts secret using the associated KMS CMK.
	// Depending on whether the secret is a string or binary, one of these fields will be populated.
	// var secretString, decodedBinarySecret string
	// secretString = ""
	// if param.SecretString != nil {
	// 	secretString = *param.Parameters.string
	// 	visit(secretString, secretFilename)
	// } else {
	// 	decodedBinarySecretBytes := make([]byte, base64.StdEncoding.DecodedLen(len(result.SecretBinary)))
	// 	len, err := base64.StdEncoding.Decode(decodedBinarySecretBytes, result.SecretBinary)
	// 	if err != nil {
	// 		log.Println("Base64 Decode Error:", err)
	// 		return
	// 	}
	// 	decodedBinarySecret = string(decodedBinarySecretBytes[:len])
	// 	visit(decodedBinarySecret, secretFilename)
	// }
}
func writeOutput(output string, name string) error {
	mountPoint := "/tmp"
	dir, file := filepath.Split(name)
	if file == "" {
		file = "secret"
	}
	err := os.MkdirAll(mountPoint + dir, os.ModePerm)
	if err != nil {
		return fmt.Errorf("error creating directory, %w", err)
	}
	if filepath.IsAbs(filepath.Join(mountPoint + dir, file)) {
		f, err := os.Create(filepath.Join(mountPoint + dir, file))
		defer f.Close()
		if err != nil {
			return fmt.Errorf("error creating file, %w", err)
		}
		f.WriteString(output)
		return nil
	}
	return fmt.Errorf("not a valid file path")
}
func visit(jsonMap map[string]interface{}, path string) error {

	i := 0

	read, err := ioutil.ReadFile("/tmp/mosaic-secret-manager.ini")
	if err != nil {
		panic(err)
	}

	fmt.Println(read)

	for s, _ := range jsonMap {
		fmt.Println(jsonMap[s])
		fmt.Println(s)
        read = []byte(strings.Replace(string(read), s , strings.Replace(fmt.Sprint(jsonMap[s]),"\"","",-1), -1))
        i++
    }
    err = ioutil.WriteFile(path, read, 0644)
	return nil
}

