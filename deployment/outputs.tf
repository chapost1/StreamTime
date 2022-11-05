output "web_api_hostname" {
  value = module.web_api.web_api_hostname
}

output "uploaded_videos_feedback_ws_url" {
  value = module.uploaded_videos_client_syncer.ws_url
}
