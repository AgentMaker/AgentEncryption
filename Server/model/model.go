package model

type RegisterParams struct {
	Username string `json:"Username"`
	Password string `json:"Password"`
}

type RegisterResp struct {
	RSAPrivate string `json:"PrivateKey"`
}

type GetModelParams struct {
	AccountInfo RegisterParams `json:"AccountInfo"`
	ID          int            `json:"ID"`
}

type ModelResp struct {
	ID             int    `json:"ID"`
	Model          string `json:"Model"`
	ModelParam     string `json:"ModelParam"`
	ModelParamInfo string `json:"ModelParamInfo"`
}
