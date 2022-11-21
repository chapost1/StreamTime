locals {
  dist        = "${path.module}/../../../services/ui/dist/"
  backendJson = "${local.dist}assets/backend.json"
}

resource "local_file" "backend_json" {
  content = jsonencode({
    url                    = var.web_api_url
    client_videos_sync_wss = var.client_videos_sync_wss
  })
  filename = local.backendJson
}

module "template_files" {
  source = "hashicorp/dir/template"

  base_dir = local.dist

  depends_on = [
    local_file.backend_json
  ]
}

resource "aws_s3_object" "static_files" {
  for_each = module.template_files.files

  bucket       = aws_s3_bucket.www_bucket.id
  key          = each.key
  content_type = each.value.content_type

  # The template_files module guarantees that only one of these two attributes
  # will be set for each file, depending on whether it is an in-memory template
  # rendering result or a static file on disk.
  source  = each.value.source_path
  content = each.value.content

  # Unless the bucket has encryption enabled, the ETag of each object is an
  # MD5 hash of that object.
  etag = each.value.digests.md5

  depends_on = [
    module.template_files.files
  ]
}
