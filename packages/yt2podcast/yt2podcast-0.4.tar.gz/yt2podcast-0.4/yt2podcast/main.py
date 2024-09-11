import requests
import datetime
import logging
import random
import re
import os
import json
import time
import webbrowser
import requests
import json
import getopt
import functools
from email import utils
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(levelname)s: %(message)s')

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15'
    }

#########
## DROPBOX
#########

def make_dropbox_refresh_token(refresh_token = None):
    if isinstance(refresh_token, type(None)):
        app_key, app_secret = get_dropbox_app()
        url = f'https://www.dropbox.com/oauth2/authorize?client_id={app_key}&' \
            f'response_type=code&token_access_type=offline'
        webbrowser.open(url)
        access_code = input("Access Code:")
        data = f'code={access_code}&grant_type=authorization_code'
        resp = requests.post('https://api.dropboxapi.com/oauth2/token',
                                data=data, auth=(app_key, app_secret))
        resp.raise_for_status()
        with open(".token", "w") as f:
            f.write(resp.json()["refresh_token"])
    else:
        with open(".token", "w") as f:
            f.write(refresh_token)
    return True

def get_dropbox_refresh_token():
    if os.path.isfile(".token"):
        with open(".token", "r") as f:
            refresh_token = f.read()
    else:
        _ = make_dropbox_refresh_token()
        refresh_token = get_dropbox_refresh_token()
    return refresh_token

def get_dropbox_app():
    if not os.path.isfile(".dropbox_app"):
        make_dropbox_app()
        return get_dropbox_app()
    with open(".dropbox_app", "r") as f:
        app_key, app_secret = f.read().split("\n")
    return app_key, app_secret

def make_dropbox_app(app_key = None, app_secret = None):
    if isinstance(app_key, type(None)):
        app_key = input("App Key:")
    if isinstance(app_secret, type(None)):
        app_secret = input("App Secret:")
    with open(".dropbox_app", "w") as f:
        f.write(f"{app_key}\n{app_secret}")

def get_dropbox_info():
    dbd = {}
    dbd["app_key"], dbd["app_secret"] = ("f5hfb4y1j7rswh7", "r2ulgpjx67q0hwh") # get_dropbox_app()
    dbd["oauth2_refresh_token"] = "zSf_mudkRvIAAAAAAAAAASKGu8xG6V1KzHKE0NXp4lmccCEpgk_Mb78V-a9xBoek" # get_dropbox_refresh_token()
    return dbd

def get_dropbox_token():
    dbd = get_dropbox_info()
    url = f"https://api.dropbox.com/oauth2/token"
    data_str = [
        f"grant_type=refresh_token",
        f"refresh_token={dbd['oauth2_refresh_token']}",
        f"client_id={dbd['app_key']}",
        f"client_secret={dbd['app_secret']}",
    ]
    data = "&".join(data_str)
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    return resp.json()

def parse_feed(filename, use_dropbox=True):
    if use_dropbox:
        token = get_dropbox_token()
        
        url = "https://api.dropboxapi.com/2/files/list_folder"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token['access_token']}",
        }
        data = {
            'path': '',
        }
        resp = requests.post(url, headers=headers, json = data)
        resp.raise_for_status()
        fhs = resp.json()["entries"]

        if filename in [fh['name'] for fh in fhs]:
            url = "https://content.dropboxapi.com/2/files/download"
            data = {
                "path": f"/{filename}"
            }
            x1 = "{"
            x2 = "}"
            headers = {
                "Authorization": f"Bearer {token['access_token']}",
                "Dropbox-API-Arg": f'{x1}"path":"/{filename}"{x2}',
            }
            resp = requests.post(url, headers=headers)
            resp.raise_for_status()
            text = resp.text
        else:
            return []
    elif os.path.isfile(filename):
        with open(filename, "r") as text_file:
            text = text_file.read()
    else:
        return []
    
    pattern = r'(<item>.*?<guid isPermaLink="false">(.*?)<\/guid>.*?<pubDate>(.*?)<\/pubDate>.*?<\/item>)'
    items = re.findall(pattern, text, flags=re.DOTALL)
    parsed_videos = [{"videoId": video_id, "xml_str": xml_str+"\n    ", "published": rfc2822_to_timestamp(publish_string)} for (xml_str, video_id, publish_string) in items]

    return parsed_videos

def save_xml_string(xml_string, filename, use_dropbox=True):
    if use_dropbox:
        token = get_dropbox_token()
        url = "https://content.dropboxapi.com/2/files/upload"
        x1 = "{"
        x2 = "}"
        headers = {
            "Content-Type": "application/octet-stream",
            "Authorization": f"Bearer {token['access_token']}",
            "Dropbox-API-Arg": f'{x1}"path":"/{filename}","mode":"overwrite"{x2}',
        }
        resp = requests.post(url, headers=headers, data = bytes(xml_string, "utf-8"))
        resp.raise_for_status()
        time.sleep(4)
        url = "https://api.dropboxapi.com/2/sharing/list_shared_links"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token['access_token']}",
        }
        data = {
            "path": "/" + filename
        }
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        if len(resp.json()["links"]) > 0:
            fp = resp.json()["links"][0]["url"].replace("&dl=0", "&raw=1")
        else:
            url = "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token['access_token']}",
            }
            data = {
                "path": "/" + filename
            }
            resp = requests.post(url, headers=headers, json=data)
            resp.raise_for_status()
            fp = resp.json()["url"].replace("&dl=0", "&raw=1")
        logging.info(f"{fp} updated.")
    else:
        with open(filename, "w") as text_file:
            text_file.write(xml_string)
        fp = os.path.abspath(filename)
    return fp

#########
## DATES
#########

def rfc2822_to_timestamp(rfc2822: str):
    x = utils.parsedate_tz(rfc2822)[:6]
    dt = datetime.datetime(*x, tzinfo = datetime.timezone.utc)
    return int(dt.timestamp())

def timestamp_to_rfc2822(timestamp: int):
    dt = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    rfc2822 = utils.format_datetime(dt)
    return rfc2822

def datetime_to_rfc2822(dt: datetime.datetime):
    return utils.format_datetime(dt)

#########
## INVIDIOUS
#########

def get_videos_from_channel(instance, channel_id, max_videos = 25):

    query = f"{instance}/api/v1/channels/{channel_id}/videos"
    videos = list()
    resp_parsed = {"videos": [None]}
    continuation_token = ""

    while len(resp_parsed["videos"]) > 0 and len(videos) < max_videos and not isinstance(continuation_token, type(None)):

        resp = requests.get(query, headers=USER_AGENT, timeout=15)
        resp.raise_for_status()
        resp_parsed = resp.json()

        videos += resp_parsed["videos"]
        continuation_token = resp_parsed.get('continuation', None)

        if not isinstance(continuation_token, type(None)):
            if "continuation" in query:
                query = re.sub(
                    pattern = "continuation=.*",
                    repl = f"continuation={continuation_token}",
                    string = query
                )
            else:
                query += f"?continuation={continuation_token}"

    if len(videos) == 0:
        raise ValueError(f"Couldn't retrieve video list from `{instance}`.")

    return videos[:max_videos]

def get_itag(instance, video_id):
    query = f"{instance}/api/v1/videos/{video_id}"
    resp = requests.get(query, headers=USER_AGENT, timeout=15)
    resp_parsed = resp.json()
    itag = int(resp_parsed["formatStreams"][-1]["itag"])
    logging.info(f"Searching itag, found {itag}")
    return itag

def get_video_url(instance, video_id, default_itag = 18):

    video_url = f'{instance}/latest_version?id={video_id}&itag={default_itag}&local=true'

    resp = requests.get(
        video_url, 
        allow_redirects=True, 
        timeout=15,
        stream=True
        )
    
    if resp.status_code == 400:
        itag = loop_func(get_itag, "instances.json", video_id)
        if itag != default_itag:
            return loop_func(get_video_url, "instances.json", video_id, default_itag=itag)

    resp.raise_for_status()
    
    if resp.headers.get("Content-Type", "None") != 'video/mp4':
        raise ValueError("Invalid Content-Type (!= 'video/mp4').")
    
    if int(resp.headers.get("Content-Length", 0)) <= 0:
        raise ValueError("Invalid Content-Length.")
    
    return video_url, resp.headers

def get_channel(instance, channel_id):
    query = f"{instance}/api/v1/channels/{channel_id}"
    resp = requests.get(query, headers=USER_AGENT, timeout=15)
    resp.raise_for_status()
    resp_parsed = resp.json()
    return resp_parsed

def combine_videos(videos, parsed_videos, mode):

    if mode == "append":
        new_videos = [x for x in videos if x["videoId"] not in [x["videoId"] for x in parsed_videos]]
        old_videos = parsed_videos
    elif mode == "overwrite":
        new_videos = videos
        old_videos = [x for x in parsed_videos if x["videoId"] not in [x["videoId"] for x in videos]]
    elif mode == "refresh":
        new_videos = parsed_videos
        old_videos = videos
    elif mode == "restart":
        new_videos = videos
        old_videos = []
    else:
        raise ValueError(f"Invalid value for `mode` ({mode}).")

    combined_videos = sorted(new_videos + old_videos, key = lambda x: x["published"], reverse=True)

    action_str = {"refresh": "update"}.get(mode, "parse")
    logging.info(f"{len(new_videos)} videos to {action_str}, {len(old_videos)} will be recycled.")

    return combined_videos

#########
## XML STRINGS
#########

def refresh_episode_xml_enclosure(xml_str, video_url, video_headers):
    content_type = video_headers["Content-Type"]
    content_length = video_headers["Content-Length"]
    enclosure_url = video_url.replace("&", "&amp;amp;")
    enclosure_pattern = r'<enclosure url="https:\/\/.*?" type=".*?" length="\d*"/>'
    new_enclosure = f'<enclosure url="{enclosure_url}" type="{content_type}" length="{content_length}"/>'
    new_xml_str = re.sub(enclosure_pattern, new_enclosure, xml_str, flags = re.DOTALL)
    return new_xml_str

def format_episode_xml(video: dict, video_url: str, video_headers: dict) -> str:

    title = video["title"].replace("&", "&amp;amp;")
    video_id = video["videoId"]
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    description = video["descriptionHtml"]
    author = video["author"].replace("&", "&amp;amp;")
    length_seconds = video["lengthSeconds"]
    
    content_type = video_headers["Content-Type"]
    content_length = video_headers["Content-Length"]
    enclosure_url = video_url.replace("&", "&amp;amp;")

    publish_string = timestamp_to_rfc2822(video["published"])

    string = f"""
    <item>
        <title>{title}</title>
        <link>{youtube_url}</link>
        <description>
            <![CDATA[{description}]]>
        </description>
        <itunes:author>{author}</itunes:author>
        <dc:creator>{author}</dc:creator>
        <guid isPermaLink="false">{video_id}</guid>
        <enclosure url="{enclosure_url}" type="{content_type}" length="{content_length}"/>
        <itunes:duration>{length_seconds}</itunes:duration>
        <pubDate>{publish_string}</pubDate>
        <itunes:explicit>no</itunes:explicit>
    </item>
"""

    return string

def format_channel_xml(channel):
    
    title = channel["author"].replace("&", "&amp;amp;")
    youtube_url = channel["authorUrl"]
    description = channel["descriptionHtml"]
    image = channel["authorThumbnails"][-1]["url"].replace("&", "&amp;amp;")

    last_build_date = datetime_to_rfc2822(datetime.datetime.now())

    string = f"""<?xml version='1.0' encoding='UTF-8'?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:podcast="https://podcastindex.org/namespace/1.0" version="2.0">
<channel>
    <title>{title}</title>
    <link>{youtube_url}</link>
    <description>
        <![CDATA[{description}]]>
    </description>
    <itunes:explicit>no</itunes:explicit>
    <docs>http://www.rssboard.org/rss-specification</docs>
    <lastBuildDate>{last_build_date}</lastBuildDate>
    <itunes:image href="{image}"/>"""

    return string

def format_end_xml():
    string = """</channel>
</rss>
"""
    return string

def update_instance_list():
    resp = requests.get("https://api.invidious.io")
    resp.raise_for_status()

    regex_pattern = r'<tr.*?>.*?href="(https:\/\/.*?)".*?>(\d{1,3}\.\d{1,3}|-).*?<\/tr>'
    listed_instances = re.findall(regex_pattern, resp.text.replace("\n", ""))
    
    if os.path.isfile("instances.json"):
        with open("instances.json") as f_in:
            instances = json.load(f_in)
    else:
        instances = dict()
    
    for listed_instance, uptime_str in listed_instances:
        if listed_instance not in instances.keys():
            try:
                uptime_int = int(float(uptime_str))
            except ValueError:
                uptime_int = 0
            logging.info(f"Adding `{listed_instance}` to `instances.json`.")
            instances[listed_instance] = uptime_int

    with open("instances.json", "w") as f_out:
        json.dump(instances, f_out)

    return instances

#########
## UTILS
#########

def is_local(url):
    if isinstance(url, list):
        return True
    url_parsed = urllib.parse.urlparse(url)
    if url_parsed.scheme in ('file', ''):
        return True
    return False

def filter_videos(videos, filters):

    tests = list()
    for filter, value in filters.items():
        if isinstance(value, type(None)):
            continue

        if filter == "minimum_duration":
            tests.append(lambda video, value=value: video["lengthSeconds"] >= value)
        elif filter == "maximum_duration":
            tests.append(lambda video, value=value: video["lengthSeconds"] <= value)
        elif filter == "maximum_age":
            tests.append(lambda video, value=value: video["published"] >= int(datetime.datetime.now().timestamp()) - (value * 86400))
        elif filter == "description_excludes_all":
            tests.append(lambda video, value=value: not all([x.lower() in video["description"].lower() for x in value]))
        elif filter == "description_excludes_any":
            tests.append(lambda video, value=value: not any([x.lower() in video["description"].lower() for x in value]))
        elif filter == "description_includes_all":
            tests.append(lambda video, value=value: all([x.lower() in video["description"].lower() for x in value]))
        elif filter == "description_includes_any":
            tests.append(lambda video, value=value: any([x.lower() in video["description"].lower() for x in value]))
        elif filter == "title_excludes_all":
            tests.append(lambda video, value=value: not all([x.lower() in video["title"].lower() for x in value]))
        elif filter == "title_excludes_any":
            tests.append(lambda video, value=value: not any([x.lower() in video["title"].lower() for x in value]))
        elif filter == "title_includes_all":
            tests.append(lambda video, value=value: all([x.lower() in video["title"].lower() for x in value]))
        elif filter == "title_includes_any":
            tests.append(lambda video, value=value: any([x.lower() in video["title"].lower() for x in value]))
        else:
            raise ValueError(f"Invalid filter `{filter}`.")

    filtered_videos = [video for video in videos if all([test(video) for test in tests])]

    logging.info(f"{len(filtered_videos)} of {len(videos)} videos left after filtering.")

    return filtered_videos

def get_channel_config(config, channel_id):
    x = [x for x in config if x["channel_id"] == channel_id]
    if len(x) > 0:
        return x[0]
    else:
        return {}
    
def loop_func(func, loop_var, *args, **kwargs):

    if not os.path.isfile(loop_var) and os.path.split(loop_var)[-1] == "instances.json":
        update_instance_list()

    with open(loop_var) as f_in:
        x = json.load(f_in)

    for var, _ in sorted(
                            list(x.items()), 
                            key=lambda x: x[1], 
                            reverse=True
                            ):
        try:
            out = func(var, *args, **kwargs)
        except Exception as e:
            logging.warning(f"`{var}` is not working [{e}].")
            out = None
            continue
        else:
            logging.debug(f"`{var}` is working!")
            x[var] = int(datetime.datetime.now().timestamp())
            with open(loop_var, "w") as f_out:
                json.dump(x, f_out)
            break

    return out

def find_channel_id(url: str):

    def __find_channel_id(instance: str, url: str):

        base = "https://www.youtube.com/"

        if base not in url:
            raise ValueError
        
        x = url.replace(base, "")

        if x[0] == "@":
            url_type = "channelHandle"
            search_string = x[1:]
        elif x[:8] == "watch?v=":
            url_type = "videoId"
            search_string = re.findall(r"watch(\?.*|&)v=(.*)(&|\b)", x)[0][1]
        elif x[:8] == "channel/":
            url_type = "authorId"
            search_string = x.replace("channel/", "")
            return search_string

        if url_type == "videoId":
            query = f"{instance}/api/v1/search?q={search_string}&type=video&sort=relevance"
        else:
            query = f"{instance}/api/v1/search?q={search_string}&type=channel&sort=relevance"

        resp = requests.get(query, headers=USER_AGENT, timeout=15)

        out = resp.json()

        return out[0]["authorId"]
    
    channel_id = loop_func(__find_channel_id, "instances.json", url)

    return channel_id

#########
## MAIN
#########

def make_or_update_channel(channel_id, use_dropbox=True, 
                           config_file = "config.json",
                           sleep_before_start = False):

    if sleep_before_start:
        time.sleep(random.randint(0, 4))

    # Make XML header.
    channel = loop_func(get_channel, "instances.json", channel_id)
    xml_string = format_channel_xml(channel)

    is_local_file = is_local(config_file)
    if isinstance(config_file, list):
        config = config_file
        channel_config = get_channel_config(config, channel_id)
    elif is_local_file:
        with open(config_file, "r") as file:
            config = list(json.load(file))
            channel_config = get_channel_config(config, channel_id)
    elif not is_local_file:
        resp = requests.get(config_file)
        resp.raise_for_status()
        config = resp.json()
        channel_config = get_channel_config(config, channel_id)
    else:
        config = []
        channel_config = {}

    if channel_config == {}:
        channel_config = {
            "name": channel["author"],
            "url": channel["authorUrl"],
            "channel_id": channel["authorId"],
            "mode": "append",
            "parse_n_videos": 25,
            "filters": {"minimum_duration": 180, "maximum_age": 7},
        }
        config.append(channel_config)
        if is_local_file:
            with open(config_file, "w") as file:
                json.dump(config, file, indent=4)
        elif not is_local_file:
            if use_dropbox:
                raise NotImplementedError()
                # dbx = get_dropbox_instance()
                # x = dbx.sharing_get_shared_link_metadata(config_file)
                # dbx.files_upload(bytes(json.dumps(config, indent = 4), "utf-8"), "/" + x.name, mode = dropbox.files.WriteMode.overwrite)
                # time.sleep(4)
            else:
                raise NotImplementedError()
        else:
            logging.warning("Can't save updated configuration.")

    logging.info(f"\n\n Updating `{channel_config['name']}`.\n")

    mode = channel_config.pop("mode")
    max_videos = channel_config.pop("parse_n_videos")
    filters = channel_config.pop("filters")
    
    filename = f"{channel_id}.txt"

    # Parse existing podcast feed.
    if mode in ["append", "overwrite", "refresh"]:
        parsed_videos = parse_feed(filename)
    elif mode in ["restart"]:
        parsed_videos = []
    else:
        raise ValueError(f"Invalid `mode` ({mode}).")

    # Get list of videos to process.
    if mode == "refresh":
        filtered_videos = []
    else:
        videos = loop_func(get_videos_from_channel, "instances.json", channel_id, max_videos=max_videos)
        filtered_videos = filter_videos(videos, filters)

    # # Combine videos.
    combined_videos = combine_videos(filtered_videos, parsed_videos, mode)

    # Process videos.
    for video in combined_videos:
        if "xml_str" in video.keys() and mode != "refresh":
            ...
        else:
            video_meta = loop_func(get_video_url, "instances.json", video["videoId"])
            if isinstance(video_meta, type(None)):
                continue
            if "xml_str" in video.keys() and mode == "refresh":
                video["xml_str"] = refresh_episode_xml_enclosure(video["xml_str"], *video_meta)
            else:
                video["xml_str"] = format_episode_xml(video, *video_meta)
        xml_string += video["xml_str"]

    xml_string += format_end_xml()

    fp = save_xml_string(
        xml_string, 
        filename, 
        use_dropbox=use_dropbox
        )

    return fp

def update_all(config_file = "config.json", threaded=True, 
               use_dropbox=True, update_parts = slice(None)):

    if is_local(config_file):
        if os.path.isfile(config_file):
            with open(config_file, "r") as file:
                config = list(json.load(file))
        else:
            raise ValueError(f"No configuration found at `{os.path.abspath(config_file)}`.")
    else:
        resp = requests.get(config_file)
        resp.raise_for_status()
        config = resp.json()

    f = functools.partial(
                    make_or_update_channel, 
                    use_dropbox=use_dropbox, 
                    config_file=config,
                    sleep_before_start = threaded,
                    )
    
    channel_ids = [x["channel_id"] for x in config][update_parts]

    if threaded:
        with ThreadPoolExecutor() as executor:
            _ = executor.map(f, channel_ids)
    else:
        _ = map(f, channel_ids)

def main(argv):

    opts, _ = getopt.getopt(argv[1:], "hc:t:d:", ["help", "config-file=", "threaded=", 
        "use-dropbox="])

    kwargs = {}
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("help me!")
        elif opt in ("-c", "--config-file"):
            kwargs["config_file"] = arg
        elif opt in ("-t", "--threaded"):
            kwargs["threaded"] = arg.lower() in ("true", "yes")
        elif opt in ("-d", "--use-dropbox"):
            kwargs["use_dropbox"] = arg.lower() in ("true", "yes")
        else:
            raise ValueError(f"Invalid option `{opt}`.")
        
    urls = update_all(**kwargs)

    return urls

if __name__ == "__main__":
    
    config_file = "https://www.dropbox.com/scl/fi/p0fioyr7cywt1ucfa1szy/config.json?rlkey=bjz3etx2ig236ne8wir1j86s5&st=et7m6zg0&raw=1"
    
    update_all(
        threaded=True, 
        update_parts=slice(0,3),
        config_file=config_file,
        )
