from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.conf import settings

from .serializers import SubmissionSerializer

class FormSubmissionView(APIView):
    def post(self, request):
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            attachments = request.FILES.get('attachment')
            affiliation = serializer.validated_data.get('affiliation', None)
            requester = serializer.validated_data.get('requester', None)
            position = serializer.validated_data.get('position', None)
            dataType = serializer.validated_data.get('dataType', None)
            formatOfDataRequested = serializer.validated_data.get('formatOfDataRequested', None)
            requestingOrganization = serializer.validated_data.get('requestingOrganization', None)
            age = serializer.validated_data.get('age', None)
            sex = serializer.validated_data.get('sex', None)
            academicBackground = serializer.validated_data.get('academicBackground', None)
            profession = serializer.validated_data.get('profession', None)
            purpose = serializer.validated_data.get('purpose', None)
            datasetName = serializer.validated_data.get('datasetName', None)
            geographicDisaggregation = serializer.validated_data.get('geographicDisaggregation', None)
            ageDisaggration = serializer.validated_data.get('ageDisaggration', None)
            sexDisaggration = serializer.validated_data.get('sexDisaggration', None)
            otherDisaggregation = serializer.validated_data.get('otherDisaggregation', None)
            phone = serializer.validated_data.get('phone', None)
            consent = serializer.validated_data.get('consent', None)

            # Compose the email
            subject = f"New Form Submission from {requester}"
            body = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            line-height: 1.8;
                            color: #444;
                            background-color: #f9f9f9;
                            padding: 20px;
                        }}
                        h2 {{
                            color: #0078D7;
                            border-bottom: 2px solid #0078D7;
                            padding-bottom: 5px;
                        }}
                        h3 {{
                            color: #0056b3;
                            margin-top: 20px;
                        }}
                        p {{
                            margin: 8px 0;
                        }}
                        .section {{
                            background-color: #ffffff;
                            border: 1px solid #ddd;
                            border-radius: 8px;
                            padding: 15px;
                            margin-bottom: 20px;
                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                        }}
                        .consent {{
                            font-style: italic;
                            color: #555;
                            background-color: #f1f1f1;
                            padding: 10px;
                            border-left: 4px solid #0078D7;
                        }}
                        .footer {{
                            margin-top: 20px;
                            font-size: 0.9em;
                            color: #666;
                        }}
                    </style>
                </head>
                <body>
                    <h2>Data/Information Request Form</h2>
                    <p>Dear Data/Information Officer,</p>
                    <p>This is a formal request for Data/Information. Below are the details:</p>
                    <div class="section">
                        <h3>Requester Details</h3>
                        <p><strong>Organization/Department/Person:</strong> {affiliation}</p>
                        <p><strong>Requester:</strong> {requester}</p>
                        <p><strong>Requesting Organization:</strong> {requestingOrganization}</p>
                        <p><strong>Position:</strong> {position}</p>
                        <p><strong>Age:</strong> {age}</p>
                        <p><strong>Sex:</strong> {sex}</p>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Academic Background:</strong> {academicBackground }</p>
                        <p><strong>Profession:</strong> {profession}</p>
                        <p><strong>Phone:</strong> {phone}</p>
                    </div>
                    <div class="section">
                        <h3>Request Details</h3>
                        <p><strong>Format of Data Requested:</strong> {formatOfDataRequested}</p>
                        <p><strong>Data Type:</strong> {dataType}</p>
                        <p><strong>Dataset Name and Year:</strong> {datasetName}</p>
                        <p><strong>Purpose:</strong> {purpose}</p>
                    </div>
                    <div class="section">
                        <h3>Data Disaggregation Details</h3>
                        <p><strong>Geographic Disaggregation:</strong> {geographicDisaggregation}</p>
                        <p><strong>Age Disaggregation:</strong> {ageDisaggration}</p>
                        <p><strong>Sex Disaggregation:</strong> {sexDisaggration}</p>
                        <p><strong>Other Disaggregation:</strong> {otherDisaggregation}</p>
                    </div>
                    <div class="section consent">
                        <h3>Consent</h3>
                        <p>I/we solemnly agree to use the data only for the stated purpose. I/we will appropriately acknowledge the data owner/source in any publication or communication. I/we will not share the data with third parties without the data owner's consent. I/we accept accountability for any breach of these terms.</p>
                        <p><strong>Consent:</strong> {consent} (By sending this email, I/we agree to the above terms.)</p>
                    </div>
                    <p class="footer">DHIS2 Public dashboard. Ministry of Health Ethiopia, powered by <a href="https://www.habtechsolution.com/" >HABTech Solutions</a> .</p>
                    <p>Best regards,</p>
                </body>
                </html>
            """
            to = [settings.EMAIL_RECIPIENT]
            email_message = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, to)
            email_message.content_subtype = "html"

            if attachments:
                # If attachments is a single file, wrap it in a list for uniform handling
                if not isinstance(attachments, list) and not hasattr(attachments, '__iter__'):
                    attachments = [attachments]
                for attachment in attachments:
                    email_message.attach(attachment.name, attachment.read(), attachment.content_type)
                    print(f"Attachment {attachment.name} added to email.")

            email_message.send(fail_silently=False)

            return Response({'message': 'Form submitted successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
