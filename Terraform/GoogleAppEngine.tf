provider "google" {
  project = "genuine-sector-443820-b5"
  region  = "us-central1"
}

# App Engine Application Configuration
resource "google_app_engine_application" "default" {
  location_id = "us-central"  # App Engine region
  
  # Optional: Define additional settings based on the provided details
  feature_settings {
    split_health_checks      = true
    use_container_optimized_os = true
  }

  # You can also specify more configuration, like custom domain or SSL, if needed.
}

# App Engine Service Account Configuration (optional)
resource "google_service_account" "gae_service_account" {
  account_id   = "genuine-sector-443820-b5"
  display_name = "App Engine Service Account"
}

# App Engine default bucket
resource "google_storage_bucket" "app_engine_default_bucket" {
  name          = "genuine-sector-443820-b5.appspot.com"
  location      = "US"
  storage_class = "STANDARD"
  uniform_bucket_level_access = true
}

# App Engine GCR Domain Configuration (optional)
resource "google_container_registry" "gcr_domain" {
  location = "US"
}

# Additional configuration for App Engine related settings
resource "google_app_engine_standard_app_version" "default" {
  version_id = "v1"  # Example version ID, replace if needed
  service    = "default"

  entrypoint {
    shell = "your_startup_command_here"  # Replace with your entrypoint or command
  }
}

# Optional: Export App Engine Application details
output "app_engine_url" {
  value = google_app_engine_application.default.default_hostname
}

output "app_engine_service_account_email" {
  value = google_service_account.gae_service_account.email
}
