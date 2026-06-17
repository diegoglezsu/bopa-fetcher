from bopa.constants import BOPA_URL, DISPOSITONS_URL


def build_link_html(date, code):
    """Build the HTML detail URL for a BOPA disposition.

    Args:
        date: Bulletin datetime object.
        code: Disposition code (e.g. "2023-11737").

    Returns:
        Full URL to the HTML detail page on the BOPA portal.
    """
    params = (
        "p_p_id=pa_sede_bopa_web_portlet_SedeBopaDispositionWeb"
        "&p_p_lifecycle=0"
        "&_pa_sede_bopa_web_portlet_SedeBopaDispositionWeb_mvcRenderCommandName=%2Fdisposition%2Fdetail"
        f"&p_r_p_dispositionText={code}"
        f"&p_r_p_dispositionReference={code}"
        f"&p_r_p_dispositionDate={date.strftime('%d%%2F%m%%2F%Y')}"
    )
    return f"{DISPOSITONS_URL}?{params}"


def build_link_pdf(date, code):
    """Build the PDF download URL for a BOPA disposition.

    Args:
        date: Bulletin datetime object.
        code: Disposition code (e.g. "2023-11737").

    Returns:
        Full URL to the PDF document on the BOPA portal.
    """
    return f"{BOPA_URL}/{date.strftime('%Y/%m/%d')}/{code}.pdf"


def build_origin(*parts):
    """Build an origin string by joining non-empty hierarchy parts.

    Args:
        *parts: Variable-length origin hierarchy components (part,
            chapter, topic, sub-author).

    Returns:
        Origin string with parts joined by " / ".
    """
    return " / ".join(part for part in parts if part)
