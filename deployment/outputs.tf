output "web_api_hostname" {
  value = module.web_api.web_api_hostname
}

output "uploaded_videos_feedback_ws_url" {
  value = module.uploaded_videos_client_syncer.ws_url
}

output "web_ui_hostmane" {
  value = module.www_ui.web_ui_hostname
}
