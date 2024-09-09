variable "pipeline_version" {
  type    = string
  default = "0.42.0"
}

variable "dashboard_version" {
  type    = string
  default = "0.31.0"
}

variable "ingress_host" {
  type    = string
  default = ""
}

variable "tls_enabled" {
  type    = bool
  default = true
}
variable "istio_enabled" {
  type    = bool
  default = false
}