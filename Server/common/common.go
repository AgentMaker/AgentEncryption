package common

import (
	"bytes"
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"log"
)

func PartEncrypt(PublicKey *rsa.PublicKey, File []byte) (data []byte, err error) {

	FileSize := len(File)

	OnceStep := PublicKey.Size() - 11

	FileOffset := 0

	var FileBuffer bytes.Buffer

	// Model Encrypt

	for FileOffset < FileSize {
		EndIndex := FileOffset + OnceStep
		if EndIndex > FileSize { // 当EndIndex比文件大的时候
			EndIndex = FileSize
		}
		// 分段加密
		Part, err := rsa.EncryptPKCS1v15(rand.Reader, PublicKey, File[FileOffset:EndIndex])
		if err != nil {
			return nil, err
		}
		FileBuffer.Write(Part)
		FileOffset = EndIndex
	}
	return FileBuffer.Bytes(), nil
}

func CreateRsaKey(bits int) (prikey string, pubkey string, err error) {
	// 生成私钥文件
	privateKey, err := rsa.GenerateKey(rand.Reader, bits)
	if err != nil {
		log.Println("CreateKeyError: ", err)
		return "", "", err
	}
	derStream := x509.MarshalPKCS1PrivateKey(privateKey)
	block := &pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: derStream,
	}
	// 向内存输出私钥
	prikey = string(pem.EncodeToMemory(block))

	//生成公钥文件
	publicKey := &privateKey.PublicKey
	derPkix, err := x509.MarshalPKIXPublicKey(publicKey)
	if err != nil {
		log.Println("CreateKeyError: ", err)
		return "", "", err
	}
	block = &pem.Block{
		Type:  "PUBLIC KEY",
		Bytes: derPkix,
	}
	// 向内存输出公钥
	pubkey = string(pem.EncodeToMemory(block))
	return
}
