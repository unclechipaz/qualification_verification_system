from datetime import timedelta
from django.utils import timezone
from qualifications.models import Certificate
from verification.models import VerificationLog

class AIFraudDetector:
    """
    AI & Heuristic Anomaly Engine for MSU Qualification Verification System.
    Analyzes search patterns, frequency, IP activity, and certificate statuses to flag fraud.
    """

    @staticmethod
    def evaluate_verification_request(query, search_type, certificate, ip_address, user_agent=None):
        """
        Calculates an Anomaly Score (0 to 100) and detects fraud indicators.
        Returns: (is_suspicious: bool, anomaly_score: int, fraud_reasons: list)
        """
        reasons = []
        score = 0
        now = timezone.now()

        # Rule 1: Search on Revoked Certificate
        if certificate and certificate.status == Certificate.Status.REVOKED:
            score += 60
            reasons.append(f"CRITICAL: Attempted verification on REVOKED certificate ({certificate.certificate_number}). Reason: {certificate.revocation_reason or 'None provided'}")

        # Rule 2: Search on Suspended Certificate
        if certificate and certificate.status == Certificate.Status.SUSPENDED:
            score += 40
            reasons.append(f"WARNING: Verification attempt on SUSPENDED certificate ({certificate.certificate_number}).")

        # Rule 3: High Rate Anomaly from IP (burst checks in last 5 minutes)
        if ip_address:
            recent_ip_count = VerificationLog.objects.filter(
                ip_address=ip_address,
                timestamp__gte=now - timedelta(minutes=5)
            ).count()

            if recent_ip_count > 15:
                score += 50
                reasons.append(f"SUSPICIOUS RATE: Automated burst scanning detected from IP {ip_address} ({recent_ip_count} requests in 5 minutes).")
            elif recent_ip_count > 7:
                score += 25
                reasons.append(f"ELEVATED FREQUENCY: High query volume from IP {ip_address} ({recent_ip_count} requests in 5 minutes).")

        # Rule 4: Query invalid format / repeated failures
        if not certificate and search_type in [VerificationLog.SearchType.CERTIFICATE_NUMBER, VerificationLog.SearchType.VERIFICATION_CODE]:
            score += 15
            reasons.append(f"INVALID IDENTIFIER: Query '{query}' does not exist in official graduate registry.")

        # Rule 5: User Agent Anomaly (Bot or script)
        if user_agent and any(bot in user_agent.lower() for bot in ['python', 'curl', 'wget', 'scraper', 'bot', 'spider']):
            score += 20
            reasons.append("AUTOMATED CLIENT: Verification request sent via automated script/bot.")

        # Cap score at 100
        score = min(score, 100)
        is_suspicious = score >= 40

        return is_suspicious, score, "; ".join(reasons) if reasons else "Normal Pattern"

    @staticmethod
    def get_fraud_analytics_summary():
        """Returns statistical overview of fraud metrics for Admin/Registrar dashboards."""
        total_verifications = VerificationLog.objects.count()
        suspicious_count = VerificationLog.objects.filter(is_suspicious=True).count()
        revoked_attempts = VerificationLog.objects.filter(certificate__status='REVOKED').count()
        high_risk_logs = VerificationLog.objects.filter(anomaly_score__gte=50).order_by('-timestamp')[:10]

        suspicious_rate = round((suspicious_count / total_verifications * 100), 1) if total_verifications > 0 else 0

        return {
            'total_verifications': total_verifications,
            'suspicious_count': suspicious_count,
            'suspicious_rate': suspicious_rate,
            'revoked_attempts': revoked_attempts,
            'high_risk_logs': high_risk_logs,
        }
