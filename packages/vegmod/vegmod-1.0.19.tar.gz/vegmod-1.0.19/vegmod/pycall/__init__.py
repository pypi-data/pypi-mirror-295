"""
vegmod.pycall exposes simple functions that can be called from the Ruby language.
Each function must only accept and return simple types (numeric, string, arrays, hashes, etc.)
"""
import os
import requests
from time import sleep
from loguru import logger
from PIL import Image
from typing import Optional, Dict, List
from vegmod import reddit

def comment_delete(comment_id : str) -> None:
    """
    Delete a comment by ID.
    """
    return reddit.comment(comment_id).delete()

def comment_edit(comment_id : str, body : str) -> None:
    """
    Edit a comment by ID.
    """
    return reddit.comment(comment_id).edit(body)

def comment_mod_approve(comment_id : str) -> None:
    """
    Approve a comment by ID.
    """
    return reddit.comment(comment_id).mod.approve()

def comment_mod_note(comment_id : str, note : str) -> None:
    """
    Create a mod note on a comment.
    """
    return reddit.comment(comment_id).mod.note(note)

def comment_mod_distinquish(comment_id : str, how : str = 'yes', sticky: bool = False) -> None:
    """
    Distinguish a comment by ID.
    
    how can be "yes", "no", "admin", or "special".
    """
    return reddit.comment(comment_id).mod.distinguish(how=how, sticky=sticky)

def comment_mod_ignore_reports(comment_id : str) -> None:
    """
    Ignore reports on a comment.
    """
    return reddit.comment(comment_id).mod.ignore_reports()

def comment_mod_lock(comment_id : str) -> None:
    """
    Lock a comment by ID.
    """
    return reddit.comment(comment_id).mod.lock()

def comment_mod_remove(comment_id : str, mod_note : str = '', spam: bool = False, reason_id: str | None = None) -> None:
    """
    Remove a comment by ID.
    """
    return reddit.comment(comment_id).mod.remove(mod_note=mod_note, spam=spam, reason_id=reason_id)

def comment_mod_send_removal_message(comment_id : str, message: str) -> None:
    """
    Send a removal message to the author of a comment.
    """
    return reddit.comment(comment_id).mod.send_removal_message(message=message)

def comment_mod_undistinguish(comment_id : str) -> None:
    """
    Undistinguish a comment by ID.
    """
    return reddit.comment(comment_id).mod.undistinguish()

def comment_mod_unignore_reports(comment_id : str) -> None:
    """
    Unignore reports on a comment.
    """
    return reddit.comment(comment_id).mod.unignore_reports()

def comment_mod_unlock(comment_id : str) -> None:
    """
    Unlock a comment by ID.
    """
    return reddit.comment(comment_id).mod.unlock()

def comment_report(comment_id : str, reason : str) -> None:
    """
    Report a comment by ID.
    """
    return reddit.comment(comment_id).report(reason)

def comment_reply(comment_id : str, body : str) -> str:
    """
    Reply to a comment with a reply.
    """
    return reddit.comment(comment_id).reply(body)

def comment_reply_distinguish_lock(comment_id : str, body : str, how : str = 'yes', sticky: bool = False) -> str:
    """
    Reply to a comment with a reply, distinguish it, and lock it.
    """
    comment = reddit.comment(comment_id).reply(body)
    comment.mod.distinguish(how=how, sticky=sticky)
    comment.mod.lock()
    return comment

def submission_delete(submission_id : str) -> None:
    """
    Delete a submission by ID.
    """
    return reddit.submission(submission_id).delete()

def submission_edit(submission_id : str, body : str) -> None:
    """
    Edit a submission by ID.
    """
    return reddit.submission(submission_id).edit(body)

def submission_mod_approve(submission_id : str) -> None:
    """
    Approve a submission by ID.
    """
    return reddit.submission(submission_id).mod.approve()

def submission_mod_create_note(submission_id : str, label : str, note : str) -> None:
    """
    Create a mod note on a submission.
    """
    return reddit.submission(submission_id).mod.create_note(label=label, note=note)

def submission_mod_distinguish(submission_id : str, how : str = 'yes', sticky: bool = False) -> None:
    """
    Distinguish a submission by ID.
    
    how can be "yes", "no", "admin", or "special".
    """
    return reddit.submission(submission_id).mod.distinguish(how=how, sticky=sticky)

def submission_mod_flair(submission_id : str, flair_template_id : str | None = None, text : str = '') -> None:
    """
    Set the flair on a submission.
    """
    return reddit.submission(submission_id).mod.flair(flair_template_id=flair_template_id, text=text)

def submission_mod_ignore_reports(submission_id : str) -> None:
    """
    Ignore reports on a submission.
    """
    return reddit.submission(submission_id).mod.ignore_reports()

def submission_mod_lock(submission_id : str) -> None:
    """
    Lock a submission by ID.
    """
    return reddit.submission(submission_id).mod.lock()

def submission_mod_nsfw(submission_id : str) -> None:
    """
    Mark a submission as NSFW.
    """
    return reddit.submission(submission_id).mod.nsfw()

def submission_mod_remove(submission_id : str, mod_note : str = '', spam: bool = False, reason_id: str | None = None) -> None:
    """
    Remove a submission by ID.
    """
    return reddit.submission(submission_id).mod.remove(mod_note=mod_note, spam=spam, reason_id=reason_id)

def submission_reply(submission_id : str, body : str) -> str:
    """
    Reply to a submission with a reply.
    """
    return reddit.submission(submission_id).reply(body)

def submission_mod_send_removal_message(submission_id : str, message: str) -> None:
    """
    Send a removal message to the author of a submission.
    """
    return reddit.submission(submission_id).mod.send_removal_message(message=message)

def submission_mod_sfw(submission_id : str) -> None:
    """
    Mark a submission as SFW.
    """
    return reddit.submission(submission_id).mod.sfw()

def submission_mod_spoiler(submission_id : str) -> None:
    """
    Mark a submission as a spoiler.
    """
    return reddit.submission(submission_id).mod.spoiler()

def submission_mod_sticky(submission_id : str, bottom: bool = True, state: bool = True) -> None:
    """
    Sticky a submission by ID.
    """
    return reddit.submission(submission_id).mod.sticky(bottom=bottom, state=state)

def submission_mod_suggested_sort(submission_id : str, sort : str = 'blank') -> None:
    """
    Set the suggested sort on a submission.
    """
    return reddit.submission(submission_id).mod.suggested_sort(sort=sort)

def submission_mod_undistinguish(submission_id : str) -> None:
    """
    Undistinguish a submission by ID.
    """
    return reddit.submission(submission_id).mod.undistinguish()

def submission_mod_unignore_reports(submission_id : str) -> None:
    """
    Unignore reports on a submission.
    """
    return reddit.submission(submission_id).mod.unignore_reports()

def submission_mod_unlock(submission_id : str) -> None:
    """
    Unlock a submission by ID.
    """
    return reddit.submission(submission_id).mod.unlock()

def submission_mod_unspoiler(submission_id : str) -> None:
    """
    Unmark a submission as a spoiler.
    """
    return reddit.submission(submission_id).mod.unspoiler()

def submission_mod_update_crowd_control_level(submission_id : str, level : int) -> None:
    """
    Update the crowd control level on a submission.
    """
    return reddit.submission(submission_id).mod.update_crowd_control_level(level=level)

def submission_report(submission_id : str, reason : str) -> None:
    """
    Report a submission by ID.
    """
    return reddit.submission(submission_id).report(reason)

def subreddit_contributor_add(subreddit_id : str, redditor_id : str) -> None:
    """
    Add a contributor to a subreddit.
    """
    return reddit.subreddit(subreddit_id).contributor.add(redditor_id)

def subreddit_contributor_exists(subreddit_id : str, redditor_id : str) -> bool:
    """
    Check if a redditor is a contributor to a subreddit.
    """
    return reddit.subreddit(subreddit_id).contributor(redditor_id) is not None

def subreddit_contributor_remove(subreddit_id : str, redditor_id : str) -> None:
    """
    Remove a contributor from a subreddit.
    """
    return reddit.subreddit(subreddit_id).contributor.remove(redditor_id)

def subreddit_mod_settings(subreddit_id) -> dict[str, str | int | bool]:
    """
    Get the settings on a subreddit.
    """
    return reddit.subreddit(subreddit_id).mod.settings()

def subreddit_mod_update(subreddit_id : str, **settings : str | int | bool) -> dict[str, str | int | bool]:
    """
    Update the settings on a subreddit.
    """
    return reddit.subreddit(subreddit_id).mod.update(**settings)

def subreddit_widgets_sidebar_delete_all(subreddit_id : str) -> None:
    """
    Delete all sidebar widgets on a subreddit.
    """
    try:
        for widget in reddit.subreddit(subreddit_id).widgets.sidebar:
            permanent_kinds = [
                'id-card'
                'moderators',
                'subreddit-rules',
            ]
            if widget.kind not in permanent_kinds:       
                try:
                    # request will silently fail if not debounced
                    sleep(3)

                    widget.mod.delete()
                except Exception as e:
                    logger.error(f"Error deleting sidebar widget: {widget}, e: {e}")
    except Exception as e:
        logger.error(f"Error deleting sidebar widgets: {e}")
    finally:
        return None

def subreddit_widgets_sidebar_delete_widget(subreddit_id: str, widget_id: str) -> None:
    """
    Delete a sidebar widget on a subreddit.
    """
    try:
        for widget in reddit.subreddit(subreddit_id).widgets.sidebar:
            if widget.id == widget_id:
                widget.mod.delete()
    except Exception as e:
        logger.error(f"Error deleting sidebar widget: {widget_id}, e: {e}")
    finally:
        return None

def subreddit_widgets_mod_upload_image(subreddit_id: str, image_url: str, link_url: str) -> Optional[Dict]:
    if '.' not in image_url:
        logger.error(f"Invalid image URL: {image_url}")
        return None

    image_url_ext = image_url.split('.')[-1]
    if image_url_ext not in ['png', 'jpg', 'jpeg']:
        logger.error(f"Invalid image EXT: {image_url}")
        return None
    
    # save the image to a file
    image_file_path = f'/tmp/praw_image_upload.{image_url_ext}'
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        with open(image_file_path, 'wb') as f:
            f.write(response.content)
        
        # extract the image dimensions using PIL
        with Image.open(image_file_path) as img:
            width, height = img.size
        
        upload_url = reddit.subreddit(
            subreddit_id
        ).widgets.mod.upload_image(
            image_file_path
        )
        
        return {
            'url': upload_url,
            'linkUrl': link_url,
            'width': width,
            'height': height,
        }
    except requests.RequestException as e:
        logger.error(f"Error downloading image: {e}")
        return None
    except IOError as e:
        logger.error(f"Error processing image file: {e}")
        return None
    finally:
        # Clean up the temporary image file
        if os.path.exists(image_file_path):
            os.remove(image_file_path)
        

def subreddit_widgets_mod_add_image_widget(subreddit_id: str, short_name: str, image_url: str, link_url: str) -> Optional[Dict]:
    """
    Add an image widget to a subreddit.
    """
    try:
        image_data = [
            subreddit_widgets_mod_upload_image(subreddit_id, image_url, link_url)
        ]
        
        styles = {
            'backgroundColor': '#FFFFFF',
            'headerColor': '#0079d3',
        }
        
        widget = reddit.subreddit(
            subreddit_id
        ).widgets.mod.add_image_widget(
            short_name=short_name, 
            data=image_data, 
            styles=styles,
            link_url=link_url
        )
        
        return widget
    except Exception as e:
        logger.error(f"Error adding image widget: {e}")
        return None

def subreddit_widgets_mod_reupload_image(subreddit_id: str, widget_id: str, image_url: str, link_url: str) -> Optional[Dict]:
    """
    Update an image widget on a subreddit.
    """
    try:
        widget = None
        for w in reddit.subreddit(subreddit_id).widgets.sidebar:
            if w.id == widget_id:
                widget = w
                break
        
        if widget is None:
            logger.error(f"Widget not found: {widget_id}")
            return None
        
        image_data = [
            subreddit_widgets_mod_upload_image(subreddit_id, image_url, link_url)
        ]
        
        widget = widget.mod.update(
            data=image_data, 
        )
        
        return widget
    except Exception as e:
        logger.error(f"Error updating image widget: {e}")
        return None

def subreddit_widgets_mod_add_community_list(subreddit_id: str, short_name: str, description: str, subreddits: List[str]) -> Optional[Dict]:
    """
    Add a community widget to a subreddit.

    Parameters:
    subreddit_id (str): The ID of the subreddit where the widget will be added.
    short_name (str): The short name for the widget.
    description (str): The description for the widget.
    subreddits (List[str]): A list of subreddit names to include in the community widget.

    Returns:
    Optional[Dict]: The response from the Reddit API if successful, None otherwise.
    """
    try:
        styles = {
            'backgroundColor': '#FFFFFF',
            'headerColor': '#0079d3',
        }
                
        return reddit.subreddit(
            subreddit_id
        ).widgets.mod.add_community_list(
            short_name=short_name, 
            description=description,
            data=subreddits,
            styles=styles
        )
    except Exception as e:
        logger.error(f"Error adding community widget: {e}")
        return None

def subreddit_widgets_mod_add_button_widget(subreddit_id: str, short_name: str, description: str, texts: List[str], urls: List[str]) -> Optional[Dict]:
    """
    Add a button widget to a subreddit.

    Parameters:
    subreddit_id (str): The ID of the subreddit where the widget will be added.
    short_name (str): The short name for the widget.
    description (str): The description for the widget.
    texts (List[str]): A list of button texts.
    urls (List[str]): A list of URLs to link to when the buttons are clicked.

    Returns:
    Optional[Dict]: The response from the Reddit API if successful, None otherwise.
    """    
    try:
        styles = {
            'backgroundColor': '#FFFFFF',
            'headerColor': '#0079d3',
        }
                
        buttons = [
            {
                'kind': 'text',
                'text': text,
                'url': url,
                'color': '#FF4500',
                'fillColor': '#FFFFFF',
                'textColor': '#000000',
            }
            for text, url in zip(texts, urls)
        ]
        return reddit.subreddit(
            subreddit_id
        ).widgets.mod.add_button_widget(
            short_name=short_name, 
            description=description,
            buttons=buttons,
            styles=styles
        ).id
    except Exception as e:
        logger.error(f"Error adding button widget: {e}")
        return None
    
def subreddit_widgets_mod_add_text_area(subreddit_id: str, short_name: str, text: str) -> Optional[Dict]:
    """
    Add a text area widget to a subreddit.

    Parameters:
    subreddit_id (str): The ID of the subreddit where the widget will be added.
    short_name (str): The short name for the widget.
    text (str): The text to display in the widget.

    Returns:
    Optional[Dict]: The response from the Reddit API if successful, None otherwise.
    """
    try:
        styles = {
            'backgroundColor': '#FFFFFF',
            'headerColor': '#0079d3',
        }
        
        # Reddit's api expects shortName casing instead of short_name when updating
        # https://praw.readthedocs.io/en/stable/code_overview/other/textarea.html
        return reddit.subreddit(
            subreddit_id
        ).widgets.mod.add_text_area(
            shortName=short_name, 
            text=text,
            styles=styles
        )
    except Exception as e:
        logger.error(f"Error adding text area widget: {e}")
        return None

def subreddit_widgets_mod_update_text_area(subreddit_id: str, widget_id: str, short_name: str, text: str) -> Optional[Dict]:
    """
    Update a text area widget on a subreddit.

    Parameters:
    subreddit_id (str): The ID of the subreddit where the widget will be updated.
    widget_id (str): The ID of the widget to update.
    short_name (str): The short name for the widget.
    text (str): The text to display in the widget.

    Returns:
    Optional[Dict]: The response from the Reddit API if successful, None otherwise.
    """
    try:
        widget = None
        for w in reddit.subreddit(subreddit_id).widgets.sidebar:
            if w.id == widget_id:
                widget = w
                break
        
        if widget is None:
            logger.error(f"Widget not found: {widget_id}")
            return None
        
        styles = {
            'backgroundColor': '#FFFFFF',
            'headerColor': '#0079d3',
        }
                
        return widget.mod.update(
            short_name=short_name, 
            text=text,
            styles=styles
        )
    except Exception as e:
        logger.error(f"Error updating text area widget: {e}")
        return None

def subreddit_widgets_mod_reorder(subreddit_id: str, widget_ids: List[str]) -> None:
    """
    Reorder widgets on a subreddit.

    Parameters:
    subreddit_id (str): The ID of the subreddit where the widgets will be reordered.
    widget_ids (List[str]): A list of widget IDs in the order they should be displayed.
    """
    try:
        # Get the existing widget order
        existing_order = [widget.id for widget in reddit.subreddit(subreddit_id).widgets.sidebar]
        new_order = []
        
        # Add the new widget IDs in the order they were provided
        for widget_id in widget_ids:
            # Only add the widget ID if it exists
            if widget_id in existing_order:
                new_order.append(widget_id)
        
        # Add any existing widget IDs that weren't provided
        for widget_id in existing_order:
            if widget_id not in new_order:
                new_order.append(widget_id)
        
        # Reorder the widgets
        reddit.subreddit(subreddit_id).widgets.mod.reorder(new_order)
    except Exception as e:
        logger.error(f"Error reordering widgets: {e}")
        return None