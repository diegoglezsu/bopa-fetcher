from bopa.constants import BOPA_URL, DISPOSITONS_URL


def build_link_html(date, code):
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
    return f"{BOPA_URL}/{date.strftime('%Y/%m/%d')}/{code}.pdf"


def build_origin(*parts):
    return " / ".join(part for part in parts if part)
