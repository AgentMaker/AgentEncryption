package core

import (
	"agentencryption/common"
	"agentencryption/model"
	"crypto/rsa"
	"crypto/x509"
	"encoding/base64"
	"encoding/pem"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	uuid "github.com/satori/go.uuid"
)

func JSONFail(ctx *gin.Context, retCode int, errorMsg string) {

	ctx.JSON(http.StatusOK, gin.H{
		"Code":      retCode,
		"Status":    "Fail",
		"RequestID": uuid.NewV4(),
		"ErrorMsg":  errorMsg,
	})
}

func JSONSuccess(ctx *gin.Context, result interface{}) {

	ctx.JSON(http.StatusOK, gin.H{
		"Code":      0,
		"Status":    "Success",
		"RequestID": uuid.NewV4(),
		"Result":    result,
	})
}

func Register(ctx *gin.Context) {
	var RegParams model.RegisterParams
	err := ctx.ShouldBindBodyWith(&RegParams, binding.JSON)
	if err != nil {
		JSONFail(ctx, -1, err.Error())
		log.Println("RequestParamsError: ", err)
		return
	}

	if RegParams.Username != "TestUser" || RegParams.Password != "test123" {
		JSONFail(ctx, -1, "Auth Error: Username or Password doesn't match.")
		log.Println("Auth Error: ", "UNAME OR PASSWD DOESN'T MATCH")
		return
	}

	prikey, pubkey, err := common.CreateRsaKey(2048) // Default: 8192

	if err != nil {
		JSONFail(ctx, -2, err.Error())
		log.Println("CreateRSAError: ", err)
		return
	}

	var Response model.RegisterResp
	Response.RSAPrivate = prikey

	err = ioutil.WriteFile("./keys/"+fmt.Sprint(RegParams.Username)+".AgentRSAPriv", []byte(prikey), 0700)

	if err != nil {
		JSONFail(ctx, -2, err.Error())
		log.Println("CreateRSAError: ", err)
		return
	}

	err = ioutil.WriteFile("./keys/"+fmt.Sprint(RegParams.Username)+".AgentRSAPub", []byte(pubkey), 0700)

	if err != nil {
		JSONFail(ctx, -2, err.Error())
		log.Println("CreateRSAError: ", err)
		return
	}

	JSONSuccess(ctx, Response)
}

func GetModel(ctx *gin.Context) {
	var GetParams model.GetModelParams
	err := ctx.ShouldBindBodyWith(&GetParams, binding.JSON)
	if err != nil {
		JSONFail(ctx, -1, err.Error())
		log.Println("RequestParamsError: ", err)
		return
	}

	if GetParams.AccountInfo.Username != "TestUser" || GetParams.AccountInfo.Password != "test123" {
		JSONFail(ctx, -1, "Auth Error: Username or Password doesn't match.")
		log.Println("Auth Error: ", "UNAME OR PASSWD DOESN'T MATCH")
		return
	}

	ModelID := fmt.Sprint(GetParams.ID)

	ModelParams, err := ioutil.ReadFile("./assets/" + ModelID + ".pdiparams")
	if err != nil {
		JSONFail(ctx, -3, err.Error())
		log.Println(err)
		return
	}
	ModelParamInfo, err := ioutil.ReadFile("./assets/" + ModelID + ".pdiparams.info")
	if err != nil {
		JSONFail(ctx, -3, err.Error())
		log.Println(err)
		return
	}
	Model, err := ioutil.ReadFile("./assets/" + ModelID + ".pdmodel")
	if err != nil {
		JSONFail(ctx, -3, err.Error())
		log.Println(err)
		return
	}

	PublicKeyFile, err := ioutil.ReadFile("./keys/" + GetParams.AccountInfo.Username + ".AgentRSAPub")
	if err != nil {
		JSONFail(ctx, -4, err.Error())
		log.Println(err)
		return
	}

	Block, _ := pem.Decode(PublicKeyFile)

	KeyInterface, err := x509.ParsePKIXPublicKey(Block.Bytes)

	if err != nil {
		JSONFail(ctx, -4, err.Error())
		log.Println(err)
		return
	}

	PublicKey := KeyInterface.(*rsa.PublicKey)

	Model, err = common.PartEncrypt(PublicKey, Model)

	if err != nil {
		JSONFail(ctx, -5, err.Error())
		log.Println(err)
		return
	}

	ModelParams, err = common.PartEncrypt(PublicKey, ModelParams)

	if err != nil {
		JSONFail(ctx, -5, err.Error())
		log.Println(err)
		return
	}

	ModelParamInfo, err = common.PartEncrypt(PublicKey, ModelParamInfo)

	if err != nil {
		JSONFail(ctx, -5, err.Error())
		log.Println(err)
		return
	}

	var ModelData model.ModelResp
	ModelData.ID = GetParams.ID
	ModelData.Model = base64.StdEncoding.EncodeToString(Model)
	ModelData.ModelParam = base64.StdEncoding.EncodeToString(ModelParams)
	ModelData.ModelParamInfo = base64.StdEncoding.EncodeToString(ModelParamInfo)

	JSONSuccess(ctx, ModelData)
}
