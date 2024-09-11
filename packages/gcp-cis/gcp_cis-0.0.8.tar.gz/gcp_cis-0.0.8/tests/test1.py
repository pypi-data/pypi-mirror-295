import unittest
from gcp_cis import gcp_client


class MyTestCase(unittest.TestCase):
    def test_authentication(self):
        sa = {
              "type": "service_account",
              "project_id": "cloud-practice-312909",
              "private_key_id": "5a715f0a92d6922acff2acf3ab89e5bcf44ed688",
              "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCyHAHXmWuiULbk\nsYruWl0ese6Z4KjfXEvqp1tyu5mVUZMR+N+Aa7EwHujCB6ookLvHRcOZOSUONH0L\nNWW4AVtZptf4sCcr28DtiaJypaTynWMuRCSwZSU7DCvbhLg0XAw5ccbzTBML2dnh\nrSziWxZNO/96g7bLLT7WWAP0DmLAVn3wMFgfdMSQ6SCxnqVSrGfwFV+IZxwXXJwm\ntrQ7o6+YbvuhKHbwI33rCGywkBh0VjoRGHH8PwO9CnRw0bm10S72yRIxL7Au9ZoT\nBXm+UyBUgk65EVDsz4nc+G0efAd6rSUOQ6TljpAIvIbapG5erwpwQpgEuFMAVLqE\nFmjL2b4fAgMBAAECggEABNemffi2dW/hjEj+o8mIwjHiPWrFpjT5l2qinaiK3dI2\n8zeJ+nemSWgKhspaKC1iY/uTyTgSUT2NSZKGrnPS/cmZRTI82zNnuADHwUg01A41\nYrRvLu1aqS1RvLxYab83uEQaPZ+Lqp6eQhJJDlDQ3WhMY0W7elcQYBfkG5/2GinA\n5QyFk6SOGDSwAeacpJw23a9X7xdHDVKshE0xGljPcgmJsXqsepaggBkjedzfJQCi\nDMD082QRWeY0lVnVGrwI3vylbDUI3IE4MyBfnKBRPUXzgf+EySrgZi50BczNNYi8\nzPARrbjTYmIArgCD8KUpk4lS+TXQNd2kDLWua/ZcMQKBgQD3wrCEVeFxRftUA3bH\n6xrG4CZxprq+8ivrwxc1t6ruW1mGwr74zd8oUbVyQ3YPuU5qQViaoSNB/OPIJ1pQ\n/Eg8qKuOdjdLrSvNvlGyEonNyAAAsRjmwhFY26cv69GFP+dmlGxEFqd7/H8z4ved\nnCwAaVQP58T8c9lvm/BFs91ZSQKBgQC4CFe1pkUeI3p0lJuIAEIjIZqeOSQU/dzV\nqXZQ+reVwXfiQqxWGNr6qddV1Px2+eCNYM15r/XOZhK4Exj6W8CxC32huNXt9IP1\nBwG31o3jmrvzLaq3tdcNTtY5VvvMdhbQmM7BW+tCIzNfcBNK8ldFz3V0lS37tMK9\nbEDtjdwEJwKBgCwJ5hhPr5fTyZ2gU/+rEYJiG1M+QJlqMFZiwgBhWjet8xbaDNnq\ntgzToT3jMdwPoxmN7fLmS38SNWbBX/NfNHPbw0q6Ro/kAxI6Dwlo9Ceosh9tWzDB\nNBYoTOper0pRFo+MOEZOBI0sT2vonvzb4pJcJn4BQ2lgKjkFbcrl8qVJAoGBAI4D\n8ht9mezuF/uLCpLjECaoMfdTxSJl3VsMkP9g2vc3+1mhdfhi6elx03irCcCOh9jS\nEP6M6TVD08I1Cpt43rRBV8vLJVuhy4r0w0Co04oGyG+amBl4u+HLKsnI9DsODgEf\nSr4wPtYk7+oARQMbDHoU5GD5FikdjwI6Xch0JosVAoGAWxmaridCfqaY4eOZS88g\nguD2A+NWnubx8vcCVXOpUgSedbmXmu+dQtujfQ8MuCeRWlilidFGVkV2l/E03Ra/\nZIkFpomPzMB0vNe13MvqBAFfLp1hNVbdRBgWTVKa1cLEJQ2VFRE1GXwKLSJatnbJ\nyKatxnMz+mtZnBbsNmJiQOo=\n-----END PRIVATE KEY-----\n",
              "client_email": "cloud-practice-bigquery-viewer@cloud-practice-312909.iam.gserviceaccount.com",
              "client_id": "107991076526924565883",
              "auth_uri": "https://accounts.google.com/o/oauth2/auth",
              "token_uri": "https://oauth2.googleapis.com/token",
              "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
              "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cloud-practice-bigquery-viewer%40cloud-practice-312909.iam.gserviceaccount.com",
              "universe_domain": "googleapis.com"
            }
        pid = 'devops-accelerators'

        try:
            client = gcp_client(service_account_info=sa, project_id=pid)
            status = True
        except Exception as e:
            status = False

        self.assertEqual(status, True)  # add assertion here

    def test_get_project_number(self):
        sa = {}
        pid = ''

        client = gcp_client(service_account_info=sa, project_id=pid)
        project_number = client.get_project_number()

        self.assertEqual('509676931471', project_number)


if __name__ == '__main__':
    unittest.main()
