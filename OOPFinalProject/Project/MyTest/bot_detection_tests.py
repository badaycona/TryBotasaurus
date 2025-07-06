from botasaurus.browser import browser, Driver

def test_cloudflare_waf(driver: Driver):
    """
    Tests bypassing Cloudflare Web Application Firewall (WAF).
    Visits a demo page protected by Cloudflare WAF.
    """
    print("Running Cloudflare WAF test...")

    driver.get("https://pcpartpicker.com/", bypass_cloudflare=True)
    driver.sleep(3)
    print("✅ Cloudflare WAF test completed")


@browser()
def run_bot_tests(driver: Driver, _):
    """
    Main function to run all bot detection tests.
    Executes various tests to check bypass capabilities against different security systems.
    """
    test_cloudflare_waf(driver)
    
    


if __name__ == "__main__":
    run_bot_tests()