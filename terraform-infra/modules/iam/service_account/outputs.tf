output "email" {
  description = "Email of the created service account"
  value       = google_service_account.this.email
}

output "name" {
  description = "Full resource ID needed for service account"
  value       = google_service_account.this.name
}
