output "mlflow-tracking-URL" {
  value = "${var.tls_enabled ? "https" : "http"}://${var.ingress_host}"
}
