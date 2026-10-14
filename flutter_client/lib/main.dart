import 'package:flutter/material.dart';
import 'services/api_service.dart';
import 'screens/browse_screen.dart';

void main() {
  runApp(const UniversalMediaApp());
}

class UniversalMediaApp extends StatelessWidget {
  const UniversalMediaApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final apiService = ApiService();

    return MaterialApp(
      title: 'Universal Media Streaming Platform',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.blue,
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF1E293B),
          elevation: 0,
        ),
      ),
      home: ServerConnectScreen(apiService: apiService),
    );
  }
}

class ServerConnectScreen extends StatefulWidget {
  final ApiService apiService;

  const ServerConnectScreen({Key? key, required this.apiService}) : super(key: key);

  @override
  State<ServerConnectScreen> createState() => _ServerConnectScreenState();
}

class _ServerConnectScreenState extends State<ServerConnectScreen> {
  final TextEditingController _ipController = TextEditingController(text: '127.0.0.1');
  final TextEditingController _portController = TextEditingController(text: '8000');

  void _connect() {
    final ip = _ipController.text.trim();
    final port = _portController.text.trim();
    widget.apiService.setBaseUrl('http://$ip:$port');

    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) => BrowseScreen(apiService: widget.apiService),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          constraints: const BoxConstraints(maxWidth: 400),
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(Icons.bolt, size: 64, color: Colors.lightBlueAccent),
              const SizedBox(height: 12),
              const Text(
                'StreamFlow Media',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              const Text(
                'Software Engineering SEA Project',
                style: TextStyle(color: Colors.grey, fontSize: 13),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 32),
              TextField(
                controller: _ipController,
                decoration: const InputDecoration(
                  labelText: 'Host Server IP',
                  hintText: 'e.g. 192.168.1.100 or 127.0.0.1',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.wifi),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _portController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Port',
                  hintText: '8000',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.numbers),
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  backgroundColor: Colors.lightBlueAccent,
                  foregroundColor: Colors.black,
                ),
                onPressed: _connect,
                child: const Text('Connect to Host Server', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
