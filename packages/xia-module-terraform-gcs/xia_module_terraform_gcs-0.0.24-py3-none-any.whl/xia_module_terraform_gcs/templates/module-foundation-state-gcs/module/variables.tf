variable "module_name" {
  type = string
  description = "Module Name"
  default = null
}

variable "config_file" {
  type = string
  description = "Project config file"
  default = ""
}

variable "landscape" {
  type = any
  description = "Landscape Configuration"
}

variable "modules" {
  type = any
  description = "Module Configuration"
}

variable "foundations" {
  type = map(any)
  description = "Foundation Configuration"
}

variable "foundation_admin_sa" {
  type = map(map(any))
  description = "Foundation admin service account dict"
}