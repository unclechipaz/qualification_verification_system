from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.permissions import IsAdminOrRegistrar
from .detector import AIFraudDetector

@login_required
def fraud_analytics_view(request):
    if not request.user.is_admin_or_registrar():
        messages.error(request, "Access denied. Admin or Registrar access required.")
        return redirect('dashboard')

    summary = AIFraudDetector.get_fraud_analytics_summary()
    return render(request, 'ai_fraud/analytics.html', {'analytics': summary})

class AIFraudAnalyticsAPIView(APIView):
    permission_classes = [IsAdminOrRegistrar]

    def get(self, request):
        summary = AIFraudDetector.get_fraud_analytics_summary()
        # Convert queryset objects to data
        summary['high_risk_logs'] = [
            {
                'id': log.id,
                'search_query': log.search_query,
                'anomaly_score': log.anomaly_score,
                'fraud_reason': log.fraud_reason,
                'ip_address': log.ip_address,
                'timestamp': log.timestamp.isoformat()
            }
            for log in summary['high_risk_logs']
        ]
        return Response(summary)
