"""
This module contains functions for serializing PRAW objects into JSON-serializable dictionaries.
"""
import time
import praw
from loguru import logger
import traceback
from vegmod.cache import Cache

def serialize(o, cache : Cache) -> dict:
    """
    Serialize a PRAW object into a JSON-serializable dictionary.
    """
    if o is None:
        return None

    s = {}
    try:
        s = _switch_case(o, cache=cache)
    except Exception as e:
        logger.error(f"Failed to serialize object={o} type={type(o).__name__} error={e}")
        traceback.print_exc()
        s["_error"] = str(e)
        s["_error_type"] = type(e).__name__
    finally:
        s["_type"] = type(o).__name__
        s["_serialized_at"] = time.time()

    return s

def serialize_list(o: list, cache : Cache = None) -> list:
    """
    Serialize a list of PRAW objects into a list of JSON-serializable dictionaries.
    """
    data = []
    for item in o:
        data.append(
            serialize(item, cache=cache)
        )
    return data

def _switch_case(obj, cache : Cache) -> dict:
    """
    Serialize a PRAW object into a JSON-serializable dictionary using a switch-case pattern.
    """
    
    # define the serialization instructions for each PRAW object type
    instruction = {
        praw.models.Submission: { 
            'function': _serialize_submission,
            'cache_key_attribute': None,
        },
        praw.models.Comment: {
            'function': _serialize_comment,
            'cache_key_attribute': None,
        },
        praw.models.Subreddit: {
            'function': _serialize_subreddit,
            'cache_key_attribute': None,
        },
        praw.models.Redditor: {
            'function': _serialize_redditor,
            'cache_key_attribute': 'name',
        },
        praw.models.RemovalReason: {
            'function': _serialize_removal_reason,
            'cache_key_attribute': None,
        },
        praw.models.Rule: {
            'function': _serialize_rule,
            'cache_key_attribute': None,
        },
        praw.models.PollOption: {
            'function': _serialize_poll_option,
            'cache_key_attribute': None,
        },
        praw.models.PollData: {
            'function': _serialize_poll_data,
            'cache_key_attribute': None,
        },
        praw.models.reddit.subreddit.SubredditRedditorFlairTemplates: {
            'function': _serialize_subreddit_flair_templates,
            'cache_key_attribute': None,
        },
        praw.models.ButtonWidget: {
            'function': _serialize_button_widget,
            'cache_key_attribute': None,
        },
        praw.models.Button: {
            'function': _serialize_button,
            'cache_key_attribute': None,
        },
        praw.models.Calendar: {
            'function': _serialize_calendar,
            'cache_key_attribute': None,
        },
        praw.models.CommunityList: {
            'function': _serialize_community_list,
            'cache_key_attribute': None,
        },
        praw.models.CustomWidget: {
            'function': _serialize_custom_widget,
            'cache_key_attribute': None,
        },
        praw.models.IDCard: {
            'function': _serialize_id_card,
            'cache_key_attribute': None,
        },
        praw.models.ImageWidget: {
            'function': _serialize_image_widget,
            'cache_key_attribute': None,
        },
        praw.models.ImageData: {
            'function': _serialize_image,
            'cache_key_attribute': None,
        },
        praw.models.Image: {
            'function': _serialize_image,
            'cache_key_attribute': None,
        },
        praw.models.ModeratorsWidget: {
            'function': _serialize_moderators_widget,
            'cache_key_attribute': None,
        },
        praw.models.PostFlairWidget: {
            'function': _serialize_post_flair_widget,
            'cache_key_attribute': None,
        },
        praw.models.RulesWidget: {
            'function': _serialize_rules_widget,
            'cache_key_attribute': None,
        },
        praw.models.TextArea: {
            'function': _serialize_text_area,
            'cache_key_attribute': None,
        },
        dict: {
            'function': _serialize_dict,
            'cache_key_attribute': None,
        },
    }[type(obj)]
    
    function = instruction['function']
    cache_key_attribute = instruction['cache_key_attribute']
    
    if cache_key_attribute is not None:
        type_string = type(obj).__name__
        attribute_value = getattr(obj, cache_key_attribute)
        cache_key = f"{type_string}_{attribute_value}"
    else:
        cache_key = None
    
    # check if the object is already in the cache
    if cache_key is not None and cache_key in cache:
        # return the cached object
        return cache[cache_key]
    
    # serialize the object
    data = function(obj, cache=cache)
    
    # add the object to the cache
    if cache_key is not None:
        cache[cache_key] = data
        
    # return the serialized object
    return data

def _serialize_dict(o: dict, cache : Cache = None):
    return o

def _serialize_submission(o: praw.models.Submission, cache : Cache = None):
    # https://praw.readthedocs.io/en/stable/code_overview/models/submission.html
    # if the submission is a poll, the poll_data attribute will be a PollData object
    # try:
    #     poll_data = serialize(o.poll_data)
    # except AttributeError:
    #     poll_data = None
    
    # if hasattr(o, "link_flair_template_id"):
    #     link_flair_template_id = o.link_flair_template_id
    # else:
    #     link_flair_template_id = None

    return {
        "author": serialize(o.author, cache=cache),
        "author_flair_text": o.author_flair_text,
        "created_utc": o.created_utc,
        "distinguished": o.distinguished,
        "edited": o.edited,
        "id": o.id,
        "is_original_content": o.is_original_content,
        "is_self": o.is_self,
        "link_flair_template_id": None, # this calls the reddit api so we don't want to do this
        "link_flair_text": "", # this calls the reddit API, so we don't want to do this
        "locked": o.locked,
        "name": o.name,
        "num_comments": o.num_comments,
        "over_18": o.over_18,
        "permalink": o.permalink,
        # "poll_data": poll_data,
        "score": o.score,
        "selftext": o.selftext,
        "spoiler": o.spoiler,
        "stickied": o.stickied,
        "title": o.title,
        "upvote_ratio": o.upvote_ratio,
        "url": o.url,
        "user_reports": serialize_list(o.user_reports),
    }

def _serialize_comment(o: praw.models.Comment, is_report : bool = False, cache : Cache = None):
    # https://praw.readthedocs.io/en/stable/code_overview/models/comment.html
    data = {
        "author": serialize(o.author, cache=cache),
        "body": o.body,
        "body_html": o.body_html,
        "created_utc": o.created_utc,
        "distinguished": o.distinguished,
        "edited": o.edited,
        "id": o.id,
        "is_submitter": o.is_submitter,
        "link_id": o.link_id,
        "parent_id": o.parent_id,
        "permalink": o.permalink,
        "score": o.score,
        "stickied": o.stickied,
        "subreddit_id": o.subreddit_id,
        "user_reports": serialize_list(o.user_reports, cache=cache),
    }
    
    return data

def _serialize_subreddit(o: praw.models.Subreddit, cache : Cache = None):
    # https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html
    return {
        "can_assign_link_flair": o.can_assign_link_flair,
        "can_assign_user_flair": o.can_assign_user_flair,
        "created_utc": o.created_utc,
        "description": o.description,
        "description_html": o.description_html,
        "display_name": o.display_name,
        "flair_templates": _serialize_subreddit_flair_templates(o.flair.templates, cache=cache),
        "id": o.id,
        "name": o.name,
        "over18": o.over18,
        "public_description": o.public_description,
        "spoilers_enabled": o.spoilers_enabled,
        "subscribers": o.subscribers,
    }

def _serialize_redditor(o: praw.models.Redditor, cache : Cache = None):
    # https://praw.readthedocs.io/en/stable/code_overview/models/redditor.html

    # if o responds to is_suspended, and it is true
    if hasattr(o, "is_suspended") and o.is_suspended:
        return {
            "name": o.name,
            "is_suspended": o.is_suspended,
            "awardee_karma": o.awardee_karma,
            "awarder_karma": o.awarder_karma,
            "is_blocked": o.is_blocked,
            "total_karma": o.total_karma,
        }

    return {
        "comment_karma": o.comment_karma,
        "total_karma": o.total_karma,
        "created_utc": o.created_utc,
        "has_verified_email": o.has_verified_email,
        "icon_img": o.icon_img,
        "id": o.id,
        "is_employee": o.is_employee,
        "is_mod": o.is_mod,
        "is_gold": o.is_gold,
        "name": o.name,
    }

def _serialize_rule(o: praw.models.Rule, cache : Cache = None):
    # https://praw.readthedocs.io/en/stable/code_overview/other/rule.html
    return {
        "created_utc": o.created_utc,
        "description": o.description,
        "kind": o.kind,
        "priority": o.priority,
        "short_name": o.short_name,
        "violation_reason": o.violation_reason,
    }

def _serialize_removal_reason(o: praw.models.RemovalReason, cache : Cache = None):
    # https://praw.readthedocs.io/en/stable/code_overview/other/removalreason.html
    return {
        "id": o.id,
        "message": o.message,
        "title": o.title,
    }

def _serialize_poll_option(o: praw.models.PollOption, cache : Cache = None):
    # https://praw.readthedocs.io/en/stable/code_overview/other/polloption.html
    return {
        "id": o.id,
        "text": o.text,
        "vote_count": o.vote_count,
    }

def _serialize_poll_data(o: praw.models.PollData, cache : Cache = None):
    # https://praw.readthedocs.io/en/stable/code_overview/other/polldata.html
    return {
        "options": [serialize(option) for option in o.options],
        "total_vote_count": o.total_vote_count,
        "voting_end_timestamp": o.voting_end_timestamp,
    }

def _serialize_subreddit_flair_templates(o: praw.models.reddit.subreddit.SubredditRedditorFlairTemplates, cache : Cache = None):
    # https://praw.readthedocs.io/en/stable/code_overview/other/subredditredditorflairtemplates.html
    templates = []
    for template in o:
        templates.append(_serialize_subreddit_flair_template(template))
    return templates

def _serialize_button_widget(o: praw.models.ButtonWidget, cache : Cache = None):
    return {
        "buttons": serialize_list(o.buttons, cache=cache),
        "description": o.description,
        "description_html": None, # o.description_html, # Apparently this is no longer an attribute from API
        "id": o.id,
        "kind": o.kind,
        "short_name": o.shortName,
        "styles": o.styles,
    }
    
def _serialize_button(o: praw.models.Button, cache : Cache = None):
    return {
        "color": o.color,
        "fill_color": o.fillColor,
        "height": o.height if hasattr(o, "height") else None,
        "hover_state": o.hoverState if hasattr(o, "hoverState") else None,
        "kind": o.kind,
        "link_url": o.linkUrl if hasattr(o, "linkUrl") else None,
        "text": o.text,
        "text_color": o.textColor,
        "url": o.url,
        "width": o.width if hasattr(o, "width") else None,
    }

def _serialize_calendar(o: praw.models.Calendar, cache : Cache = None):
    return {
        "configuration": o.configuration,
        "data": o.data,
        "id": o.id,
        "kind": o.kind,
        "requires_sync": o.requiresSync,
        "short_name": o.shortName,
        "styles": o.styles,
    }

def _serialize_community_list(o: praw.models.CommunityList, cache : Cache = None):
    return {
        "data": _serialize_subreddit_list(o.data, cache=cache),
        "id": o.id,
        "kind": o.kind,
        "short_name": o.shortName,
        "styles": o.styles,
    }

def _serialize_custom_widget(o: praw.models.CustomWidget, cache : Cache = None):
    return {
        "css": o.css,
        "height": o.height,
        "id": o.id,
        "imageData": serialize_list(o.imageData, cache=cache),
        "kind": o.kind,
        "short_name": o.shortName,
        "styles": o.styles,
        "stylesheet_url": o.stylesheetUrl,
        "text": o.text,
        "text_html": o.textHtml,
    }

def _serialize_id_card(o: praw.models.IDCard, cache : Cache = None):
    return {
        "currently_viewing_count": o.currentlyViewingCount,
        "currently_viewing_text": o.currentlyViewingText,
        "description": o.description,
        "id": o.id,
        "kind": o.kind,
        "short_name": o.shortName,
        "styles": o.styles,
        "subscribers_count": o.subscribersCount,
        "subscribers_text": o.subscribersText,
    }

def _serialize_image_widget(o: praw.models.ImageWidget, cache : Cache = None):
    return {
        "data": serialize_list(o.data, cache=cache),
        "id": o.id,
        "kind": o.kind,
        "short_name": o.shortName,
        "styles": o.styles,
    }

def _serialize_image(o: praw.models.ImageData | praw.models.Image, cache : Cache = None):
    return {
        "height": o.height,
        "link_url": o.linkUrl,
        "url": o.url,
        "width": o.width,
    }

def _serialize_moderators_widget(o: praw.models.ModeratorsWidget, cache : Cache = None):
    return {
        "id": o.id,
        "kind": o.kind,
        "mods": serialize_list(o.mods, cache=cache),
        "short_name": o.shortName,
        "styles": o.styles,
    }

def _serialize_post_flair_widget(o: praw.models.PostFlairWidget, cache : Cache = None):
    return {
        "display": o.display,
        "id": o.id,
        "kind": o.kind,
        "order": o.order,
        "short_name": o.shortName,
        "styles": o.styles,
        "templates": o.templates
    }

def _serialize_rules_widget(o: praw.models.RulesWidget, cache : Cache = None):
    return {
        "data": serialize_list(o.data, cache=cache),
        "display": o.display,
        "id": o.id,
        "kind": o.kind,
        "short_name": o.shortName,
        "styles": o.styles,
    }

def _serialize_text_area(o: praw.models.TextArea, cache : Cache = None):
    return {
        "id": o.id,
        "kind": o.kind,
        "short_name": o.shortName,
        "styles": o.styles,
        "text": o.text,
        "text_html": o.textHtml,
    }
    
def _serialize_subreddit_list(o: list[praw.models.Subreddit], cache : Cache = None):
    # extract ids from the list of subreddits
    return [subreddit.id for subreddit in o]

def _serialize_subreddit_flair_template(o: dict):
    return o
