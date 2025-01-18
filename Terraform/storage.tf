resource "google_storage_bucket" "docu_storage" {
  name          = "docu_storage"
  location      = "EU"               # Multi-region
  storage_class = "STANDARD"

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 7    # Matches retentionDurationSeconds: '604800' (7 days in seconds)
    }
  }

  public_access_prevention = "enforced"
}
