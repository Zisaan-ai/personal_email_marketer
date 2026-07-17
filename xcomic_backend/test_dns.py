
import dns.resolver
try:
    print('Testing dns.resolver...')
    records = dns.resolver.resolve('gmail.com', 'MX')
    for r in records:
        print(r.exchange, r.preference)
except Exception as e:
    import traceback
    traceback.print_exc()
