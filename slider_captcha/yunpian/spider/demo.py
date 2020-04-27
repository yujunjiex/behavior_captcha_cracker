# coding: utf-8
import requests

p = {
    'cb': "cijcrdkuc7g",
    "i": "FwZe64kkEFQWufBdWx7NKXl5JW8K0iDfkr1wYbfft37oNweb+N6VMBAb3t9ifc0rspun5jTcpnSnzP+C4C6Q/jDgUpILZd2xJ9Eq4I0D2VcemaKs66h3XNs22jgJCYocut95kP93qr+Cd90PykoWY503YSbgn6kM+d6VcS/2D7U7uMmdRoMiLoqW1wYBuB3HdfhOnahShkmxvuCne3SDzrir1txEaOYMOVBSacsJgOvAPvmQe1IQKh9F/uCr/eQLTzUKyPY3M8uA+fqQvlHhtnxcvHZ9KhTqFP2yyV21gM2PTe0L0UrWa6aTghS1MHvcuWVeVrLfD2WwZDO7QhBE3d4UfnCOwZqv14cvQRp0eI4ZQ25CkW/GI4sACXYrcbm1MRMxHNC3A91iOEYcM51sbQVZlEW0ctFtHXfmuSH7JWFlNO7/gcCPwW4kAhzTuZ9lMlwMDQ1n2v1NbUMrBepxb9hhoEAihoS7GuNqU/Mrb7XFfas5oumNdT8B93ygEgAD0ByDKeJov0jGuslqhd3dq2zFPw879G+Eh1l9QVBRrqb+RAdbMRmfw0F9iq60OaOPSsZiwvX33P+A/yNsaK7Vr0713nNUFS2qI3aFzDUm6uU2mXYX+M1BoPH9OgGsdKSe7wnGqMNbA+kJIamj/luHk72ko+vk8ly7b3mWugkJKurf2US8dWcZx2IXZu3AB9bf",
    "k": "gzQay9nESXSqo735yHwRx4d9jy1gCg+p4Z5ls5MoO0z9I4yaWs1cstFIH81xFlVY4Zebtrb/ibVkCEHrhOQkGvw+qijgrdDEImXQv5YIzLDmMtxWOySGfGwEgbMfZHM5MRidldzEXFQEN6wE2J+oe5y/f9j+uovFPaa2LclXdmA=",
    'captchaId': '974cd565f11545b6a5006d10dc324281'
}

resp = requests.get(url='https://captcha.yunpian.com/v1/jsonp/captcha/get',
                    params={
                        'cb': 'cijcrdkuc7g',
                        'i': 'cF0z9WDu2mGGXNymXiC8OpS8zZHxWU565+kxHTClZjcE2yPXAHU1LqfLkqlcQIUVD8PT2P4xCV5cW7BrfJwiJfnXJiUDCwSwSCV57pS7AmFOFBQi6XW5YKwBrV5vwLXEnTL09Nn3EsOvqeNY3uDD/72lfGGwRwJ2cwsql2Dd9vgmBeLiCfdLnERYnR+2JhHz5+Jp7QPIuZn7o5f8MjK0NfTqK4jtMVIFeZm5RVZda0rZKdNjKyqhi6IvL/YUYvobOjArFesqhOFk3flKKGVfU1tyZqjAsBQl9IAFpcTfbYaa4dQWiYwpz1GKoQVn6vZcrcSSj+IR6aCRmhYiZkIxluG0STI03qcwSX4AfxF/Zp8r50XZmmH4+aGh2AYysJs1j7JyNIc0roFSHtxxdCVWMeYuispB1D3ibeq8PAPV3caOKehI+YcoJfGYww22BY4qbX3Agn8jqx+x5EyxYgey4jxJreviBhsatAh87r9dLjfZO+sDnJFJMU7OqAyfzZ/NlJ06r9kE6bU4XRl9VHSpJ8jGEelUBjmXZQOhomv+Jlo9jnpuUD9p5xTaPI056VXpHDf411bTDEI61TU0kiglbfQDUgKuARSgqMgi2ohpeuFSPG+IM6htJ7dFlOZNFuUhtuL1jbGaCCEtfV91NkwfBjJ6Ze+vlFid3CYP9ObSjU0SqJGcKw/O7QGyWjyjnSlbjvHgqMc4g73L/kDiW2HU65y/QmP69aNL0orzFTz94wIB7lGeVUZ1c0HUgwlI4wDPbJ9BcRh7aIAwGpNrkmop+WimrOIQMJxyCvS54yfT8Z0=',
                        'k': 'OmOUqTHwlZiPPL/pORDNTRbpcZ88kcA9YtDfUYueBWL2HlwZEiZ4iGdVPG/+3SieE+HTVjasT0UXjVNTqCau8WsF0AFndijBkptCu8A5k0fGp6EgAEVxZsfyR9RcbtIncm5XMH9IP5mSpdDT8MRFxC2ajrRRDWtlurllplcqcsM=',
                        'captchaId': '974cd565f11545b6a5006d10dc324281'
                    })

print(resp.text)

