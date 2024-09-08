variable "module_name" {
  type = string
  description = "Module Name"
  default = ""
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

variable "foundations" {
  type = map(any)
  description = "Foundation Configuration"
}
