import re
from typing import List, Optional, Dict

from .https import (
    channel_about,
    streams_data,
    uploads_data,
    channel_playlists,
    upcoming_videos,
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
        obj = extract_initial_data(self.__html)
        meta = obj["metadata"]["channelMetadataRenderer"]
        detailed_meta = (
            obj
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
        # is_verified = (
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
        is_verified = "'metadataBadgeRenderer': {'icon': {'iconType': 'CHECK_CIRCLE_THICK'}" in str(obj)
        # is_live = (
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
        is_live = "'text': {'runs': [{'text': 'LIVE'}]" in str(obj)
        data = {
            "id": meta["externalId"],
            "name": meta["title"],
            "description": detailed_meta["description"],
            "subscribers": detailed_meta["subscriberCountText"].split(" ")[0],
            "views": detailed_meta["viewCountText"]
            .replace(" views", "")
            .replace(",", ""),
            "country": detailed_meta["country"],
            "url": "https://www.youtube.com/channel/" + meta["externalId"],
            "avatars": obj["header"]["pageHeaderRenderer"]["content"][
                "pageHeaderViewModel"
            ].get(
                "image",
                {
                    "decoratedAvatarViewModel": {
                        "avatar": {"avatarViewModel": {"image": {"sources": []}}}
                    }
                },
            )["decoratedAvatarViewModel"]
            ["avatar"]
            ["avatarViewModel"]
            ["image"]
            ["sources"],
            "banners": obj["header"]["pageHeaderRenderer"]["content"][
                "pageHeaderViewModel"
            ].get(
                "banner", 
                {
                    "imageBannerViewModel": {
                        "image": {"sources": []}
                    }
                }
            )["imageBannerViewModel"]["image"]["sources"],
            "rss_url": meta.pop("rssUrl"),
            "video_count": int(
                detailed_meta.pop("videoCountText").replace(",", "").split(" ")[0]
            ),
            "custom_url": detailed_meta["canonicalChannelUrl"],
            "joined_date": detailed_meta["joinedDateText"]["content"].replace(
                "Joined ", ""
            ),
            "socials": [
                link["channelExternalLinkViewModel"]["link"]["content"]
                for link in detailed_meta.get("links", [])
            ],
            "keywords": obj["microformat"]["microformatDataRenderer"]["tags"],
            "is_family_safe": meta["isFamilySafe"],
            "available_country_codes": meta["availableCountryCodes"],
            "verified": is_verified,
            "live": is_live,
        }
        return data

    @property
    def streaming_now(self) -> Optional[str]:
        """
        Fetches the id of currently streaming video

        Returns
        -------
        str | None
            The id of the currently streaming video or None
        """
        streams = self.current_streams
        return streams[0] if streams else None

    @property
    def current_streams(self) -> Optional[List[str]]:
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
            if f"vi/{id_}/hqdefault_live.jpg" in streams_data(raw)
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

    def uploads(self, limit: int = 20) -> Optional[List[str]]:
        """
        Fetches the ids of all uploaded videos

        Parameters
        ----------
        limit : int
            The number of videos to fetch, defaults to 20

        Returns
        -------
        List[str] | None
            The ids of uploaded videos or None
        """
        return dup_filter(
            Patterns.upload_ids.findall(uploads_data(self._target_url)), limit
        )

    @property
    def last_uploaded(self) -> Optional[str]:
        """
        Fetches the id of the last uploaded video

        Returns
        -------
        str | None
            The id of the last uploaded video or None
        """
        ids = self.uploads()
        return ids[0] if ids else None

    @property
    def upcoming(self) -> Optional[Video]:
        """
        Fetches the upcoming video

        Returns
        -------
        Video | None
            The upcoming video or None
        """
        raw = upcoming_videos(self._target_url)
        if not Patterns.upcoming_check.search(raw):
            return None
        upcoming = Patterns.upcoming.findall(raw)
        return Video(upcoming[0]) if upcoming else None

    @property
    def upcomings(self) -> Optional[List[str]]:
        """
        Fetches the upcoming videos

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

    @property
    def playlists(self) -> Optional[List[str]]:
        """
        Fetches the ids of all playlists

        Returns
        -------
        List[str] | None
            The ids of all playlists or None
        """
        return dup_filter(
            Patterns.playlists.findall(channel_playlists(self._target_url))
        )
