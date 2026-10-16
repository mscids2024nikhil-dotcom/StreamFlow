import 'package:flutter/material.dart';
import '../models/media_item.dart';
import '../services/api_service.dart';
import 'player_screen.dart';

class BrowseScreen extends StatefulWidget {
  final ApiService apiService;

  const BrowseScreen({Key? key, required this.apiService}) : super(key: key);

  @override
  State<BrowseScreen> createState() => _BrowseScreenState();
}

class _BrowseScreenState extends State<BrowseScreen> {
  List<MediaItem> _mediaList = [];
  bool _isLoading = true;
  String _filterType = '';
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadMedia();
  }

  Future<void> _loadMedia() async {
    setState(() => _isLoading = true);
    final items = await widget.apiService.fetchMedia(
      mediaType: _filterType.isEmpty ? null : _filterType,
      search: _searchController.text.trim(),
    );
    setState(() {
      _mediaList = items;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Universal Media Stream'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadMedia,
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Search audio, video, movies...',
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                suffixIcon: IconButton(
                  icon: const Icon(Icons.clear),
                  onPressed: () {
                    _searchController.clear();
                    _loadMedia();
                  },
                ),
              ),
              onSubmitted: (_) => _loadMedia(),
            ),
          ),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Row(
              children: [
                ChoiceChip(
                  label: const Text('All'),
                  selected: _filterType.isEmpty,
                  onSelected: (selected) {
                    if (selected) {
                      setState(() => _filterType = '');
                      _loadMedia();
                    }
                  },
                ),
                const SizedBox(width: 8),
                ChoiceChip(
                  label: const Text('🎬 Videos'),
                  selected: _filterType == 'video',
                  onSelected: (selected) {
                    setState(() => _filterType = selected ? 'video' : '');
                    _loadMedia();
                  },
                ),
                const SizedBox(width: 8),
                ChoiceChip(
                  label: const Text('🎵 Audio'),
                  selected: _filterType == 'audio',
                  onSelected: (selected) {
                    setState(() => _filterType = selected ? 'audio' : '');
                    _loadMedia();
                  },
                ),
              ],
            ),
          ),
          const SizedBox(height: 8),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _mediaList.isEmpty
                    ? const Center(child: Text('No media found on host.'))
                    : ListView.builder(
                        itemCount: _mediaList.length,
                        itemBuilder: (context, index) {
                          final item = _mediaList[index];
                          final isVideo = item.mediaType == 'video';
                          return ListTile(
                            leading: CircleAvatar(
                              child: Icon(isVideo ? Icons.movie : Icons.music_note),
                            ),
                            title: Text(item.title, maxLines: 1, overflow: TextOverflow.ellipsis),
                            subtitle: Text('${item.categoryName ?? 'General'} • ${(item.fileSize / (1024 * 1024)).toStringAsFixed(1)} MB'),
                            trailing: const Icon(Icons.play_arrow),
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => PlayerScreen(
                                    item: item,
                                    apiService: widget.apiService,
                                  ),
                                ),
                              );
                            },
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }
}
