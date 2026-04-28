def handle_command(text):
    global current_mode

    text = text.lower().strip()

    # ─────────────────────────────────────
    # EXIT / CONTROL
    # ─────────────────────────────────────
    if any(x in text for x in ["exit", "shutdown friday", "terminate"]):
        return "exit"

    if any(x in text for x in ["sleep", "go to sleep", "goodbye"]):
        return "sleep"

    # ─────────────────────────────────────
    # YOUTUBE MODE
    # ─────────────────────────────────────
    if "youtube" in text:
        query = (
            text.replace("open youtube", "")
                .replace("search youtube for", "")
                .replace("play", "")
                .replace("on youtube", "")
                .replace("youtube", "")
                .strip()
        )

        current_mode = "youtube"
        return skills.open_youtube(query if query else None)

    # YouTube controls (context-aware)
    if current_mode == "youtube":

        if "click first video" in text:
            return skills.click_first_video()

        if "scroll down" in text:
            return skills.scroll_down()

        if "scroll up" in text:
            return skills.scroll_up()

        if "pause" in text or "play" in text:
            return skills.pause_video()

        if "next video" in text:
            return vision.click_element("next video button")

        if "skip ad" in text:
            return vision.click_element("skip ad button")

    # ─────────────────────────────────────
    # VISION CONTROL (GLOBAL)
    # ─────────────────────────────────────
    if text.startswith("click"):
        target = text.replace("click", "").strip()
        if target:
            return vision.click_element(target)
        else:
            return "What should I click Boss?"

    if "what is on screen" in text or "analyze screen" in text:
        path = vision.capture_screen()
        return vision.analyze_screen(path, "Describe everything visible on this screen")

    # ─────────────────────────────────────
    # NEWS MODE
    # ─────────────────────────────────────
    if "news" in text or "current affairs" in text:
        current_mode = "browser"
        skills.open_news()
        headlines = skills.get_headlines()
        return headlines

    # ─────────────────────────────────────
    # GOOGLE SEARCH
    # ─────────────────────────────────────
    if any(x in text for x in ["search", "google"]):
        query = (
            text.replace("search for", "")
                .replace("search", "")
                .replace("google", "")
                .strip()
        )

        if query:
            return skills.google_search(query)
        else:
            return "What should I search Boss?"

    # ─────────────────────────────────────
    # GENERAL WEB ACTIONS
    # ─────────────────────────────────────
    if "scroll down" in text:
        return vision.click_element("scroll bar down")

    if "scroll up" in text:
        return vision.click_element("scroll bar up")

    # ─────────────────────────────────────
    # MODE RESET
    # ─────────────────────────────────────
    if "close browser" in text or "exit youtube" in text:
        current_mode = None
        try:
            skills.driver.quit()
        except:
            pass
        return "Closed browser Boss."

    # ─────────────────────────────────────
    # FALLBACK AI (BRAIN)
    # ─────────────────────────────────────
    return think(text)