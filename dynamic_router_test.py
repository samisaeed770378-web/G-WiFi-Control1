from router_models import (
    vendors,
    models_for_vendor,
    firmwares_for,
    find_router,
)
from router_discovery import discover_router


def choose(title, items):
    print()
    print("=" * 45)
    print(title)
    print("=" * 45)

    for i, item in enumerate(items, 1):
        print(f"{i}) {item}")

    while True:
        try:
            n = int(input("\nاختيارك: "))
            if 1 <= n <= len(items):
                return items[n - 1]
        except ValueError:
            pass

        print("اختيار غير صحيح، حاول مرة أخرى.")


def main():
    print()
    print("==============================================")
    print("        G-WiFi Control - Dynamic Test")
    print("==============================================")

    # 1. الشركة
    vendor = choose("اختر الشركة", vendors())

    # 2. الموديل يتغير حسب الشركة
    model_list = models_for_vendor(vendor)

    if not model_list:
        print("لا توجد موديلات مسجلة لهذه الشركة.")
        return

    model = choose(
        f"موديلات {vendor}",
        model_list
    )

    # 3. Firmware يتغير حسب الشركة + الموديل
    firmware_list = firmwares_for(vendor, model)

    if not firmware_list:
        print("لا توجد إصدارات Firmware مسجلة.")
        return

    firmware = choose(
        f"Firmware لـ {vendor} / {model}",
        firmware_list
    )

    # 4. استخراج Adapter + API من قاعدة البيانات
    router = find_router(
        vendor,
        model,
        firmware
    )

    if not router:
        print("لم يتم العثور على تعريف الراوتر.")
        return

    print()
    print("==============================================")
    print("ROUTER PROFILE")
    print("==============================================")
    print("Company  :", router.vendor)
    print("Model    :", router.model)
    print("Firmware :", router.firmware)
    print("Adapter  :", router.adapter)
    print("API      :", router.api)

    # 5. بيانات الاتصال
    host = input(
        "\nRouter URL/IP (مثال http://192.168.1.1): "
    ).strip()

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if not host:
        print("يجب إدخال عنوان الراوتر.")
        return

    # 6. API Discovery
    print()
    print("==============================================")
    print("API DISCOVERY")
    print("==============================================")
    print("جاري اختبار نقاط الإدارة المعروفة...")

    result = discover_router(
        vendor,
        model,
        firmware,
        host,
        username,
        password
    )

    if result.get("api_detected"):
        print("API STATUS : DETECTED")
        print("ENDPOINT   :", result.get("endpoint"))
        print("HTTP STATUS:", result.get("http_status"))
    else:
        print("API STATUS : NOT DETECTED")
        print()
        print("لم يتم العثور على API معروفة لهذا التعريف.")
        print("يمكن أن يكون الراوتر يستخدم واجهة مختلفة.")
        return

    # 7. Adapter
    print()
    print("==============================================")
    print("ADAPTER")
    print("==============================================")
    print("Selected Adapter:", router.adapter)

    # 8. إنشاء الـAdapter الحقيقي من RouterManager
    try:
        from router_manager import RouterManager

        manager = RouterManager()

        manager.connect(
            vendor=vendor,
            model=model,
            firmware=firmware,
            host=host,
            username=username,
            password=password,
        )

        print("CONNECTION : OK")

        # 9. الوظائف المدعومة فقط
        supported = manager.get_supported_features()

        print()
        print("==============================================")
        print("SUPPORTED FEATURES")
        print("==============================================")

        if supported:
            for feature in supported:
                print("✓", feature)
        else:
            print("لا توجد وظائف مؤكدة حاليًا.")

    except Exception as e:
        print()
        print("CONNECTION : FAILED")
        print("REASON     :", e)

    print()
    print("==============================================")
    print("DYNAMIC TEST FINISHED")
    print("==============================================")


if __name__ == "__main__":
    main()
