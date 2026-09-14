import 'package:flutter/material.dart';

void main() {
  runApp(const NetworkManagementApp());
}

class NetworkManagementApp extends StatelessWidget {
  const NetworkManagementApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Network Management - سامي الصنوي',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0B0F19),
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  void _onButtonPressed(String title) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('جاري تشغيل وظيفة: $title بكفاءة عالية...', style: const TextStyle(fontWeight: FontWeight.bold)),
        duration: const Duration(seconds: 1),
        backgroundColor: Colors.blueAccent,
      ),
    );
  }

  void _handleDnaAction(BuildContext context, String actionName) {
    Navigator.of(context).pop();

    String description = '';
    IconData actionIcon = Icons.info;

    switch (actionName) {
      case 'Network Management':
        description = 'إدارة البنية التحتية للشبكة، التحكم في المسارات، وتوزيع الأحمال.';
        actionIcon = Icons.router;
        break;
      case 'Device Discovery':
        description = 'جاري مسح الشبكة والبحث عن الأجهزة المتصلة وتصنيفها تلقائياً.';
        actionIcon = Icons.devices;
        break;
      case 'Provisioning':
        description = 'توزيع ملفات التكوين وتجهيز أجهزة الشبكة الجديدة وتشغيلها عن بُعد.';
        actionIcon = Icons.settings_suggest;
        break;
      case 'Assurance':
        description = 'مراقبة صحة الأداء الشامل للشبكة وتحليل تجربة المستخدم والتطبيقات لحظياً.';
        actionIcon = Icons.verified;
        break;
      case 'Monitoring':
        description = 'مراقبة حية لاستهلاك النطاق الترددي (Bandwidth) وحالة الحزم وسرعة التدفق.';
        actionIcon = Icons.monitor_heart;
        break;
      case 'Telemetry':
        description = 'جمع البيانات والقياسات الحية من الأجهزة وتحليلها عبر التدفقات الذكية.';
        actionIcon = Icons.analytics;
        break;
      case 'Security':
        description = 'تفعيل سياسات الأمان، كشف التهديدات السيبرانية، وعزل الأجهزة المشبوهة.';
        actionIcon = Icons.security;
        break;
      case 'Policy Management':
        description = 'إدارة سياسات الوصول (Access Control) وتطبيق سياسات الجودة والتحكم بالصلاحيات.';
        actionIcon = Icons.policy;
        break;
      case 'Workworkflows':
        description = 'تنفيذ مهام سير العمل الآلية المجدولة لتقليل الأخطاء البشرية وتسريع الصيانة.';
        actionIcon = Icons.alt_route;
        break;
      case 'Applications':
        description = 'مراقبة وتحديد أولويات التطبيقات الحيوية داخل الشبكة لضمان عدم توقفها.';
        actionIcon = Icons.apps;
        break;
      case 'Issues & Troubleshooting':
        description = 'فحص الأخطاء وتشخيص الأعطال الجذرية تلقائياً مع اقتراح حلول فورية للإصلاح.';
        actionIcon = Icons.healing;
        break;
      case 'Analytics':
        description = 'تحليل البيانات التاريخية والحالية للشبكة للتنبؤ بالمشاكل المستقبلية وتخطيط التوسعات.';
        actionIcon = Icons.bar_chart;
        break;
      default:
        description = 'جاري معالجة الطلب بنجاح.';
        actionIcon = Icons.check_circle;
    }

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1F2937),
        title: Row(
          children: [
            Icon(actionIcon, color: Colors.purpleAccent, size: 28),
            const SizedBox(width: 12),
            Expanded(child: Text(actionName, style: const TextStyle(color: Colors.white, fontSize: 18))),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(description, style: const TextStyle(color: Colors.white70, fontSize: 15, height: 1.4)),
            const SizedBox(height: 15),
            const LinearProgressIndicator(color: Colors.purpleAccent, backgroundColor: Colors.black26),
            const SizedBox(height: 10),
            const Text(' الحالة: تم التنفيذ بنجاح بكفاءة وسرعة عالية.', style: TextStyle(color: Colors.greenAccent, fontSize: 12)),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('حسناً', style: TextStyle(color: Colors.purpleAccent, fontSize: 16)),
          ),
        ],
      ),
    );
  }

  void _showDnaCenterDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          backgroundColor: const Color(0xFF2C2C2C),
          title: Row(
            children: const [
              Icon(Icons.hub, color: Colors.purpleAccent),
              SizedBox(width: 10),
              Text('DNA Center', style: TextStyle(color: Colors.white, fontSize: 20)),
            ],
          ),
          content: SizedBox(
            width: double.maxFinite,
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  _buildDnaOption(context, 'Network Management', Icons.router),
                  _buildDnaOption(context, 'Device Discovery', Icons.devices),
                  _buildDnaOption(context, 'Provisioning', Icons.settings_suggest),
                  _buildDnaOption(context, 'Assurance', Icons.verified),
                  _buildDnaOption(context, 'Monitoring', Icons.monitor_heart),
                  _buildDnaOption(context, 'Telemetry', Icons.analytics),
                  _buildDnaOption(context, 'Security', Icons.security),
                  _buildDnaOption(context, 'Policy Management', Icons.policy),
                  _buildDnaOption(context, 'Workworkflows', Icons.alt_route),
                  _buildDnaOption(context, 'Applications', Icons.apps),
                  _buildDnaOption(context, 'Issues & Troubleshooting', Icons.healing),
                  _buildDnaOption(context, 'Analytics', Icons.bar_chart),
                ],
              ),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('إغلاق', style: TextStyle(color: Colors.purpleAccent, fontSize: 16)),
            ),
          ],
        );
      },
    );
  }

  Widget _buildDnaOption(BuildContext context, String title, IconData icon) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: InkWell(
        borderRadius: BorderRadius.circular(6),
        onTap: () => _handleDnaAction(context, title),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 8),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.05),
            borderRadius: BorderRadius.circular(6),
          ),
          child: Row(
            children: [
              Icon(icon, color: Colors.blueAccent, size: 20),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  title,
                  style: const TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.w500),
                ),
              ),
              const Icon(Icons.arrow_forward_ios, color: Colors.white24, size: 14),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('إدارة الشبكة ... قوة في يديك', style: TextStyle(fontSize: 16)),
        centerTitle: true,
        backgroundColor: const Color(0xFF111827),
        leading: const Padding(
          padding: EdgeInsets.all(8.0),
          child: CircleAvatar(
            backgroundColor: Colors.purpleAccent,
            child: Icon(Icons.hub, color: Colors.white, size: 20),
          ),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                Expanded(child: _buildButton('QoS', Colors.blue, 60)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('SMTP', Colors.blue, 60)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('RMON', Colors.blue, 60)),
              ],
            ),
            const SizedBox(height: 10),
            _buildHeaderButton('بروتوكولات مراقبة WAN 📡', Colors.deepPurple),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _buildButton('SNMP', Colors.deepPurple, 70)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('Wireless IDS', Colors.deepPurple, 70)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('Wi-Fi Scan', Colors.deepPurple, 70)),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _buildButton('DHCP', Colors.deepPurple, 70)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('RADIUS', Colors.deepPurple, 70)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('NetFlow', Colors.deepPurple, 70)),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _buildButton('QoS', Colors.deepPurple, 70)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('DNS', Colors.deepPurple, 70)),
              ],
            ),
            const SizedBox(height: 15),
            _buildHeaderButton('صيانة LAN / WAN 🛠️', Colors.orange[800]!),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _buildButton('Backup', Colors.orange, 70)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('Firmware', Colors.orange, 70)),
                const SizedBox(width: 8),
                Expanded(child: _>_buildButton('إعادة تشغيل', Colors.orange, 70)),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _buildButton('Optimize', Colors.orange, 70)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('Health Check', Colors.orange, 70)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('Config', Colors.orange, 70)),
              ],
            ),
            const SizedBox(height: 15),
            _buildHeaderButton('اكتشاف أعطال الشبكة بالذكاء الاصطناعي 🧠', Colors.pink),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _buildButton('WAN تحليل AI', Colors.deepPurple, 60)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('LAN تحليل AI', Colors.blue, 60)),
              ],
            ),
            const SizedBox(height: 20),
            _buildHeaderButton('مهام الشبكة المتقدمة 🚀', Colors.cyan),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _buildButton('Gateway', Colors.blue, 65)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('Subnet', Colors.blue, 65)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('المحلي IP', Colors.blue, 65)),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _buildButton('Ping', Colors.blue, 65)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('الأجهزة المحلية', Colors.blue, 65)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('DNS', Colors.blue, 65)),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _buildButton('Port Test', Colors.blue, 65)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('Traceroute', Colors.blue, 65)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('Speed Test', Colors.blue, 65)),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _buildButton('دخول إداري WAN', Colors.deepPurple, 65)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('دخول إداري LAN', Colors.blue, 65)),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(child: _buildButton('السجل Log', Colors.blue, 65)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('الأجهزة', Colors.blue, 65)),
                const SizedBox(width: 8),
                Expanded(child: _buildButton('المستخدمون', Colors.blue, 65)),
              ],
            ),
            const SizedBox(height: 10),
            InkWell(
              onPressed: () => _showDnaCenterDialog(context),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 16),
                decoration: BoxDecoration(
                  color: Colors.blue,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: const Center(
                  child: Text(
                    '🧬 DNA Center',
                    style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 10),
            InkWell(
              onPressed: () => _showDnaCenterDialog(context),
              child: Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.cyan,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  children: const [
                    Text('🧬 DNA Center', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                    SizedBox(height: 4),
                    Text('اضغط لإظهار جميع الوظائف', style: TextStyle(color: Colors.white70, fontSize: 12)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 25),
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFF1F2937),
                borderRadius: BorderRadius.compiler if needed,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: Colors.blueAccent.withOpacity(0.3)),
              ),
              child: Column(
                children: const [
                  Text(
                    '• Network Management •',
                    style: TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.bold, fontSize: 14),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'المطور: المهندس سامي الصنوي',
                    style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.bold),
                  ),
                  SizedBox(height: 4),
                  Text(
                    'Email: samisaeed770378@gmail.com',
                    style: TextStyle(color: Colors.cyanAccent, fontSize: 13),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'إدارة الشبكة ... قوة في يديك',
                    style: TextStyle(color: Colors.grey, fontSize: 13, fontStyle: FontStyle.italic),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildButton(String text, Color color, double height) {
    return SizedBox(
      height: height,
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: color,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
          elevation: 2,
        ),
        onPressed: () => _onButtonPressed(text),
        child: Text(
          text,
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold),
        ),
      ),
    );
  }

  Widget _buildHeaderButton(String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 10),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(6),
      ),
      child: Center(
        child: Text(
          text,
          style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ),
    );
  }
}
