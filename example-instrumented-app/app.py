import tracing
import metrics

import time
import random

def main():
  try:
    while True:
      metrics.emit_metrics()
      tracing.emit_trace()
      time.sleep(random.randint(3, 7))
  finally:
    pass

if __name__ == "__main__":
  main()