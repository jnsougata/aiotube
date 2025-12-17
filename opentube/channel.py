import re
from typing import List, Optional, Dict, Any

from .https import (
    channel_about,
    streams_data,
    uploads_data,
    channel_playlists,
    upcoming_videos, shorts_data,
)
from .patterns import _ChannelPatterns as Patterns
from .utils import dup_filter, extract_initial_data
from .video import Video


class Channel:

    _HEAD = "https://www.youtube.com/channel/"
    _CUSTOM = "https://www.youtube.com/c/"
    _USER = "https://www.youtube.com/"

    def __init__(self, channel_id: str):
        """
        Represents a YouTube channel

        Parameters
        ----------
        channel_id : str
            The id or url or custom url or user id of the channel
        """
        pattern = re.compile("UC(.+)|c/(.+)|@(.+)")
        results = pattern.findall(channel_id)
        if not results:
            self._usable_id = channel_id
            self._target_url = self._CUSTOM + channel_id
        elif results[0][0]:
            self._usable_id = results[0][0]
            self._target_url = self._HEAD + "UC" + results[0][0]
        elif results[0][1]:
            self._usable_id = results[0][1]
            self._target_url = self._CUSTOM + results[0][1]
        elif results[0][2]:
            self._usable_id = results[0][2]
            self._target_url = self._USER + "@" + results[0][2]
        self.__html = channel_about(self._target_url)
        self.__obj = extract_initial_data(self.__html)
        self.__meta = self.__obj["metadata"]["channelMetadataRenderer"]
        self.__detailed_meta = (
            self.__obj
            ["onResponseReceivedEndpoints"]
            [0]
            ["showEngagementPanelEndpoint"]
            ["engagementPanel"]
            ["engagementPanelSectionListRenderer"]
            ["content"]
            ["sectionListRenderer"]
            ["contents"]
            [0]
            ["itemSectionRenderer"]
            ["contents"]
            [0]
            ["aboutChannelRenderer"]
            ["metadata"]
            ["aboutChannelViewModel"]
        )

    @property
    def id(self) -> str:
        """
        Returns the channel id

        Returns
        -------
        str
            The channel id
        """
        return self.__meta["externalId"]

    @property
    def name(self) -> str:
        """
        Returns the channel name

        Returns
        -------
        str
            The channel name
        """
        return self.__meta["title"]

    @property
    def description(self) -> str:
        """
        Returns the channel description

        Returns
        -------
        str
            The channel description
        """
        return self.__detailed_meta["description"]

    @property
    def subscribers(self) -> str:
        """
        Returns the channel subscriber count

        Returns
        -------
        str
            The channel subscriber count
        """
        return self.__detailed_meta["subscriberCountText"].split(" ")[0]

    @property
    def views(self) -> str:
        """
        Returns the channel view count

        Returns
        -------
        str
            The channel view count
        """
        return self.__detailed_meta["viewCountText"].replace(" views", "").replace(",", "")

    @property
    def country(self) -> str:
        """
        Returns the channel country

        Returns
        -------
        str
            The channel country
        """
        return self.__detailed_meta.get("country", "")

    @property
    def url(self) -> str:
        """
        Returns the channel url

        Returns
        -------
        str
            The channel url
        """
        return "https://www.youtube.com/channel/" + self.__meta["externalId"]

    @property
    def avatars(self) -> List[Dict[str, Any]]:
        """
        Returns the channel avatars

        Returns
        -------
        List[Dict[str, Any]]
            The channel avatars in different resolutions
        """
        return self.__obj["header"]["pageHeaderRenderer"]["content"][
            "pageHeaderViewModel"
        ].get(
            "image",
            {
                "decoratedAvatarViewModel": {
                    "avatar": {"avatarViewModel": {"image": {"sources": []}}}
                }
            },
        )["decoratedAvatarViewModel"]["avatar"]["avatarViewModel"]["image"]["sources"]

    @property
    def banners(self) -> List[Dict[str, Any]]:
        """
        Returns the channel banners

        Returns
        -------
        List[Dict[str, Any]]
            The channel banners in different resolutions
        """
        return self.__obj["header"]["pageHeaderRenderer"]["content"][
            "pageHeaderViewModel"
        ].get(
            "banner",
            {
                "imageBannerViewModel": {
                    "image": {"sources": []}
                }
            }
        )["imageBannerViewModel"]["image"]["sources"]

    @property
    def rss_url(self) -> str:
        """
        Returns the channel RSS url

        Returns
        -------
        str
            The channel RSS url
        """
        return self.__meta["rssUrl"]

    @property
    def video_count(self) -> int:
        """
        Returns the total number of videos uploaded in the channel

        Returns
        -------
        int
            The total number of videos uploaded in the channel
        """
        return int(
            self.__detailed_meta["videoCountText"].replace(",", "").split(" ")[0]
        )

    @property
    def custom_url(self) -> str:
        """
        Returns the channel custom url

        Returns
        -------
        str
            The channel custom url
        """
        return self.__detailed_meta["canonicalChannelUrl"]

    @property
    def creation_date(self) -> str:
        """
        Returns the channel joined date

        Returns
        -------
        str
            The channel joined date
        """
        return self.__detailed_meta["joinedDateText"]["content"].replace(
            "Joined ", ""
        )

    @property
    def socials(self) -> List[str]:
        """
        Returns the channel social links

        Returns
        -------
        List[str]
            The channel social links
        """
        return [
            link["channelExternalLinkViewModel"]["link"]["content"]
            for link in self.__detailed_meta.get("links", [])
        ]

    @property
    def keywords(self) -> List[str]:
        """
        Returns the channel keywords

        Returns
        -------
        List[str]
            The channel keywords
        """
        return self.__obj["microformat"]["microformatDataRenderer"]["tags"]

    @property
    def family_safe(self) -> bool:
        """
        Returns whether the channel is marked as family safe

        Returns
        -------
        bool
            True if the channel is marked as family safe, False otherwise
        """
        return self.__meta["isFamilySafe"]

    @property
    def available_country_codes(self) -> List[str]:
        """
        Returns the list of country codes where the channel is available

        Returns
        -------
        List[str]
            The list of country codes where the channel is available
        """
        return self.__meta["availableCountryCodes"]

    @property
    def verified(self) -> bool:
        """
        Returns whether the channel is verified

        Returns
        -------
        bool
            True if the channel is verified, False otherwise
        """
        # return (
        #     self.__obj
        #     ["header"]
        #     ["pageHeaderRenderer"]
        #     ["content"]
        #     ["pageHeaderViewModel"]
        #     ["title"]
        #     ["dynamicTextViewModel"]
        #     ["text"].get(
        #         "attachmentRuns",
        #         [
        #             {
        #                 "element": {
        #                     "type": {
        #                         "imageType": {
        #                             "image": {
        #                                 "sources": [
        #                                     {"clientResource": {"imageName": "_"}}
        #                                 ]
        #                             }
        #                         }
        #                     }
        #                 }
        #             }
        #         ],
        #     )
        #     [0]
        #     ["element"]
        #     ["type"]
        #     ["imageType"]
        #     ["image"]
        #     ["sources"]
        #     [0]
        #     ["clientResource"]
        #     ["imageName"]
        # ) == "CHECK_CIRCLE_FILLED"
        return "'metadataBadgeRenderer': {'icon': {'iconType': 'CHECK_CIRCLE_THICK'}" in str(self.__obj)

    @property
    def live(self) -> bool:
        """
        Returns whether the channel is currently live streaming

        Returns
        -------
        bool
            True if the channel is currently live streaming, False otherwise
        """
        # return (
        #     self.__obj
        #     ["contents"]
        #     ["twoColumnBrowseResultsRenderer"]
        #     ["tabs"]
        #     [0]
        #     ["tabRenderer"]
        #     ["content"]
        #     ["sectionListRenderer"]
        #     ["contents"]
        #     [0]
        #     ["channelFeaturedContentRenderer"]
        #     ["items"]
        #     [0]
        #     ["thumbnailOverlays"]
        #     [0]
        #     ["thumbnailOverlayTimeStatusRenderer"]
        #     ["text"]
        #     ["runs"]
        #     [0]
        #     ["text"]
        # ) == "LIVE"
        return "'text': {'runs': [{'text': 'LIVE'}]" in str(self.__obj)

    @property
    def metadata(self) -> Dict[str, any]:
        """
        Returns channel metadata in a dict format

        Returns
        -------
        Dict
            Channel metadata containing the following keys:
            id, name, subscribers, views, country, custom_url, avatar, banner, url, description, socials etc.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "subscribers": self.subscribers,
            "views": self.views,
            "country": self.country,
            "url": self.url,
            "avatars": self.avatars,
            "banners": self.banners,
            "rss_url": self.rss_url,
            "video_count": self.video_count,
            "custom_url": self.custom_url,
            "creation_date": self.creation_date,
            "socials": self.socials,
            "keywords": self.keywords,
            "family_safe": self.family_safe,
            "available_country_codes": self.available_country_codes,
            "verified": self.verified,
            "live": self.live
        }

    @property
    def streaming_now(self) -> Optional[List[str]]:
        """
        Fetches the ids of all ongoing streams

        Returns
        -------
        List[str] | None
            The ids of all ongoing streams or None
        """
        raw = streams_data(self._target_url)
        filtered_ids = dup_filter(Patterns.stream_ids.findall(raw))
        if not filtered_ids:
            return None
        return [
            id_
            for id_ in filtered_ids
            if f'vi/{id_}/hqdefault_live.jpg' in streams_data(raw)
        ]

    @property
    def old_streams(self) -> Optional[List[str]]:
        """
        Fetches the ids of all old or completed streams

        Returns
        -------
        List[str] | None
            The ids of all old or completed streams or None
        """
        raw = streams_data(self._target_url)
        filtered_ids = dup_filter(Patterns.stream_ids.findall(raw))
        if not filtered_ids:
            return None
        return [
            id_ for id_ in filtered_ids if f"vi/{id_}/hqdefault_live.jpg" not in raw
        ]

    @property
    def last_streamed(self) -> Optional[str]:
        """
        Fetches the id of the last completed livestream

        Returns
        -------
        str | None
            The id of the last livestreamed video or None
        """
        ids = self.old_streams
        return ids[0] if ids else None

    def shorts(self) -> Optional[Dict[str, Any]]:
        """
        Fetches uploaded shorts and their basic metadata

        Returns
        -------
        Dict[str, Any] | None
            A dict containing basic metadata of uploaded shorts or None
        """
        try:
            initial_data = extract_initial_data(shorts_data(self._target_url))
            shorts = (
                initial_data
                ["contents"]
                ["twoColumnBrowseResultsRenderer"]
                ["tabs"][2]["tabRenderer"]["content"]
                ["richGridRenderer"]["contents"]
            )
        except KeyError:
            return None
        data = {}
        for raw_short in shorts:
            if not raw_short.get("richItemRenderer"):
                continue
            short = raw_short["richItemRenderer"]["content"]["shortsLockupViewModel"]
            thumbnail = short["thumbnailViewModel"]["thumbnailViewModel"]["image"]["sources"][0]
            video_id = thumbnail["url"].split("/vi/")[1].split("/")[0]
            data[video_id] = {
                "id": video_id,
                "url": "https://www.youtube.com/shorts/" + video_id,
                "title": short["overlayMetadata"]["primaryText"]["content"],
                "views": short["overlayMetadata"]["secondaryText"]["content"].replace(" views", "").replace(",", ""),
                "thumbnail": thumbnail,
            }
        return data

    def videos(self) -> Optional[Dict[str, Any]]:
        """
        Fetches upto 30 uploaded videos and their basic metadata

        Returns
        -------
        Dict[str, Any] | None
            A dict containing basic metadata of uploaded videos or None
        """
        try:
            initial_data = extract_initial_data(uploads_data(self._target_url))
            videos = (
                initial_data
                ["contents"]
                ["twoColumnBrowseResultsRenderer"]
                ["tabs"][1]["tabRenderer"]["content"]
                ["richGridRenderer"]["contents"]
            )
        except KeyError:
            return None
        data = {}
        for raw_video in videos:
            if not raw_video.get("richItemRenderer"):
                continue
            v = raw_video["richItemRenderer"]["content"]["videoRenderer"]
            video_id = v["videoId"]
            data[video_id] = {
                "title": v["title"]["runs"][0]["text"],
                "id": video_id,
                "url": "https://www.youtube.com/watch?v=" + video_id,
                "description": v.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", ""),
                "views": v.get("viewCountText", {}).get("simpleText", "0").replace(" views", "").replace(",", ""),
                "published": v.get("publishedTimeText", {}).get("simpleText", ""),
                "duration": v.get("lengthText", {}).get("simpleText", ""),
                "thumbnails": v["thumbnail"]["thumbnails"],
            }
        return data

    @property
    def last_uploaded(self) -> Optional[Dict[str, Any]]:
        """
        Fetches the id of the last uploaded video

        Returns
        -------
        Dict[str, Any] | None
            The id of the last uploaded video or None
        """
        videos = self.videos()
        return list(videos.values())[0] if videos else None

    @property
    def upcoming(self) -> Optional[List[str]]:
        """
        Fetches the upcoming video ids

        Returns
        -------
        List[str] | None
            The ids of upcoming videos or None
        """
        raw = upcoming_videos(self._target_url)
        if not Patterns.upcoming_check.search(raw):
            return None
        video_ids = Patterns.upcoming.findall(raw)
        return video_ids

    @staticmethod
    def __format_playlist_data(raw: Dict[str, Any]):
        model = raw["lockupViewModel"]
        video_count_text = None
        overlays = model["contentImage"]["collectionThumbnailViewModel"]["primaryThumbnail"]["thumbnailViewModel"]["overlays"]
        for overlay in overlays:
            if overlay["thumbnailOverlayBadgeViewModel"]["thumbnailBadges"][0]["thumbnailBadgeViewModel"]["badgeStyle"] == "THUMBNAIL_OVERLAY_BADGE_STYLE_DEFAULT":
                video_count_text = overlay["thumbnailOverlayBadgeViewModel"]["thumbnailBadges"][0]["thumbnailBadgeViewModel"]["text"]
                break
        return {
            "id": model["contentId"],
            "title": model["metadata"]["lockupMetadataViewModel"]["title"]["content"],
            "video_count": video_count_text.replace(" videos", "") if video_count_text else "0",
            "thumbnail": model["contentImage"]["collectionThumbnailViewModel"]["primaryThumbnail"]["thumbnailViewModel"]["image"]["sources"][0],
            "url": "https://www.youtube.com/playlist?list=" + model["contentId"],
        }

    def playlists(self) -> Optional[List[Dict[str, Any]]]:
        """
        Fetches the basic metadata of some public playlists.

        Returns
        -------
        List[Dict[str, Any]] | None
            The basic metadata of all playlists or None
        """
        obj = extract_initial_data(
            channel_playlists(self._target_url))["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
        playlist_tab = None
        for tab in obj:
            if not tab.get("tabRenderer"):
                continue
            if tab["tabRenderer"]["title"] == "Playlists":
                playlist_tab = tab
                break
        if not playlist_tab:
            return None
        raw_playlists = (
            playlist_tab
            ["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]
            ["itemSectionRenderer"]["contents"][0]["gridRenderer"]["items"]
        )
        return [self.__format_playlist_data(item) for item in raw_playlists]
