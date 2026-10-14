class MediaItem {
  final int mediaId;
  final String title;
  final String filePath;
  final String mediaType;
  final String mimeType;
  final int duration;
  final int fileSize;
  final int? categoryId;
  final String? categoryName;

  MediaItem({
    required this.mediaId,
    required this.title,
    required this.filePath,
    required this.mediaType,
    required this.mimeType,
    required this.duration,
    required this.fileSize,
    this.categoryId,
    this.categoryName,
  });

  factory MediaItem.fromJson(Map<String, dynamic> json) {
    return MediaItem(
      mediaId: json['media_id'],
      title: json['title'],
      filePath: json['file_path'],
      mediaType: json['media_type'],
      mimeType: json['mime_type'],
      duration: json['duration'] ?? 0,
      fileSize: json['file_size'] ?? 0,
      categoryId: json['category_id'],
      categoryName: json['category_name'],
    );
  }

  String get streamUrl => '/api/media/$mediaId/stream';
}
