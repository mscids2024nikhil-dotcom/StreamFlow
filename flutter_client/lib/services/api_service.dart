import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/media_item.dart';
import '../models/user.dart';

class ApiService {
  String baseUrl = 'http://127.0.0.1:8000';
  String? token;
  User? currentUser;

  void setBaseUrl(String url) {
    baseUrl = url.endsWith('/') ? url.substring(0, url.length - 1) : url;
  }

  Future<bool> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      token = data['access_token'];
      currentUser = User.fromJson(data['user']);
      return true;
    }
    return false;
  }

  Future<bool> register(String username, String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'email': email, 'password': password}),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      token = data['access_token'];
      currentUser = User.fromJson(data['user']);
      return true;
    }
    return false;
  }

  Future<List<MediaItem>> fetchMedia({String? mediaType, int? categoryId, String? search}) async {
    final queryParameters = <String, String>{};
    if (mediaType != null) queryParameters['media_type'] = mediaType;
    if (categoryId != null) queryParameters['category_id'] = categoryId.toString();
    if (search != null && search.isNotEmpty) queryParameters['search'] = search;

    final uri = Uri.parse('$baseUrl/api/media').replace(queryParameters: queryParameters);
    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final List items = data['items'];
      return items.map((e) => MediaItem.fromJson(e)).toList();
    }
    return [];
  }

  Future<void> saveHistory(int mediaId, int position) async {
    if (token == null) return;
    await http.post(
      Uri.parse('$baseUrl/api/history'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({'media_id': mediaId, 'last_position': position}),
    );
  }

  String getStreamUrl(int mediaId) {
    return '$baseUrl/api/media/$mediaId/stream';
  }
}
