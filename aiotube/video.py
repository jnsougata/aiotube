import re

from .https import video_data
from typing import Dict, Any
from enum import Enum

from .utils import extract_initial_data


class _EngagementPanelType(Enum):
    comments = "engagement-panel-comments-section"
    description = "engagement-panel-structured-description"

def find_engagement_panel(data: Dict[str, Any], panel_type_id: str) -> Dict[str, Any]:
    for panel in data["engagementPanels"]:
        if panel["engagementPanelSectionListRenderer"].get("panelIdentifier", "") == panel_type_id:
            return panel["engagementPanelSectionListRenderer"]
    return {}


class Video:

    _HEAD = "https://www.youtube.com/watch?v="

    def __init__(self, video_id: str):
        """
        Represents a YouTube video

        Parameters
        ----------
        video_id : str
            The id or url of the video
        """
        pattern = re.compile(r".be/(.*?)$|=(.*?)$|^(\w{11})$")
        self._matched_id = (
            pattern.search(video_id).group(1)
            or pattern.search(video_id).group(2)
            or pattern.search(video_id).group(3)
        )
        if self._matched_id:
            self._url = self._HEAD + self._matched_id
            self._video_data = (
                extract_initial_data(video_data(self._matched_id))
            )
            import json

            print(json.dumps(self._video_data, indent=4))
        else:
            raise ValueError("invalid video id or url")

    def __repr__(self):
        return f"<Video {self._url}>"

    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Fetches video metadata in a dict format

        Returns
        -------
        Dict
            Video metadata in a dict format containing keys: title, id, views, duration, author_id,
            upload_date, url, thumbnails, tags, description
        """
        info_section = self._video_data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"]
        primary_info = info_section[0]["videoPrimaryInfoRenderer"]
        secondary_info = info_section[1]["videoSecondaryInfoRenderer"]
        comments_section = find_engagement_panel(self._video_data, _EngagementPanelType.comments.value)
        data = {
            "title": primary_info["title"]["runs"][0]["text"],
            "id": self._matched_id,
            "views": primary_info["viewCount"]["videoViewCountRenderer"]["originalViewCount"],
            "comments": (
                comments_section["header"]["engagementPanelTitleHeaderRenderer"]["contextualInfo"]["runs"][0]["text"]
                if comments_section
                else None
            ),
            "likes": (
                primary_info["videoActions"]["menuRenderer"]["topLevelButtons"][0]
                ["segmentedLikeDislikeButtonViewModel"]["likeCountEntity"]["expandedLikeCountIfIndifferent"]["content"]
            ),
            "owner": {
                "title": secondary_info["owner"]["videoOwnerRenderer"]["title"]["runs"][0]["text"],
                "id": secondary_info["owner"]["videoOwnerRenderer"]["title"]["runs"][0]["navigationEndpoint"][
                    "browseEndpoint"
                ]["browseId"],
                "avatars": secondary_info["owner"]["videoOwnerRenderer"]["thumbnail"]["thumbnails"],
                "subscribers": secondary_info["owner"]["videoOwnerRenderer"]["subscriberCountText"]["simpleText"],
            },
            "published": primary_info["dateText"]["simpleText"],
            "url": f"https://www.youtube.com/watch?v={self._matched_id}",
            "thumbnail": f"https://i.ytimg.com/vi/{self._matched_id}/maxresdefault.jpg",
            # "tags": metadata.get("keywords"), # agh! this is not available in the initial data
            # "streamed": metadata["isLiveContent"], # agh! this is not available in the initial data
            # "duration": metadata["lengthSeconds"], # agh! this is not available in the initial data
            "description": secondary_info["attributedDescription"]["content"],
        }
        # try:
        #     data["genre"] = genre_pattern.search(self._video_data).group(1)
        # except AttributeError:
        #     data["genre"] = None
        return data
