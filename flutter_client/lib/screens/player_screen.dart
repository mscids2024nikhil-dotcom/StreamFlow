import 'package:flutter/material.dart';
import '../models/media_item.dart';
import '../services/api_service.dart';

class PlayerScreen extends StatefulWidget {
  final MediaItem item;
  final ApiService apiService;

  const PlayerScreen({Key? key, required this.item, required this.apiService}) : super(key: key);

  @override
  State<PlayerScreen> createState() => _PlayerScreenState();
}

class _PlayerScreenState extends State<PlayerScreen> {
  bool _isPlaying = false;
  double _currentPosition = 0;
  late final String _streamUrl;

  @override
  void initState() {
    super.initState();
    _streamUrl = widget.apiService.getStreamUrl(widget.item.mediaId);
    _isPlaying = true;
  }

  void _togglePlayPause() {
    setState(() {
      _isPlaying = !_isPlaying;
    });
    // In real app, sends play/pause to video_player/audioplayers controller
  }

  void _onSeek(double value) {
    setState(() {
      _currentPosition = value;
    });
    widget.apiService.saveHistory(widget.item.mediaId, value.toInt());
  }

  @override
  Widget build(BuildContext context) {
    final isVideo = widget.item.mediaType == 'video';

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.item.title),
      ),
      body: Column(
        children: [
          Expanded(
            child: Container(
              color: Colors.black87,
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      isVideo ? Icons.videocam : Icons.audiotrack,
                      size: 96,
                      color: Colors.white70,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Streaming over HTTP Range',
                      style: const TextStyle(color: Colors.white60, fontSize: 14),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      _streamUrl,
                      style: const TextStyle(color: Colors.lightBlueAccent, fontSize: 12),
                    ),
                  ],
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            child: Column(
              children: [
                Text(
                  widget.item.title,
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  '${widget.item.mediaType.toUpperCase()} • ${widget.item.categoryName ?? 'Media'}',
                  style: const TextStyle(color: Colors.grey),
                ),
                const SizedBox(height: 20),
                Slider(
                  value: _currentPosition,
                  min: 0,
                  max: (widget.item.duration > 0 ? widget.item.duration.toDouble() : 100.0),
                  onChanged: _onSeek,
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    IconButton(
                      iconSize: 36,
                      icon: const Icon(Icons.replay_10),
                      onPressed: () => _onSeek((_currentPosition - 10).clamp(0, 9999)),
                    ),
                    const SizedBox(width: 20),
                    FloatingActionButton(
                      onPressed: _togglePlayPause,
                      child: Icon(_isPlaying ? Icons.pause : Icons.play_arrow),
                    ),
                    const SizedBox(width: 20),
                    IconButton(
                      iconSize: 36,
                      icon: const Icon(Icons.forward_10),
                      onPressed: () => _onSeek(_currentPosition + 10),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
