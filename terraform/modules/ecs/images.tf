# web_api

data "archive_file" "archive_web_api_dir" {
  type        = "zip"
  source_dir  = "${path.module}/../../../packages/api/"
  output_path = "web_api.zip"
}

resource "null_resource" "web_api_ecr_image" {
  triggers = {
    src_hash = "${data.archive_file.archive_web_api_dir.output_sha}"
  }

  provisioner "local-exec" {
    command = <<EOF
           docker login ${var.ecr_token_proxy_endpoint} -u AWS -p ${var.ecr_token_password}
           cd ${path.module}/../../../packages/api
           docker build -t ${module.ecr.repository_url}:${local.web_api_image_tag} .
           docker push ${module.ecr.repository_url}:${local.web_api_image_tag}
       EOF
  }
  depends_on = [
    var.ecr_authorization_token
  ]
}

data "aws_ecr_image" "web_api_ecr_image" {
  depends_on = [
    null_resource.web_api_ecr_image
  ]
  repository_name = module.ecr.repository_name
  image_tag       = local.web_api_image_tag
}
