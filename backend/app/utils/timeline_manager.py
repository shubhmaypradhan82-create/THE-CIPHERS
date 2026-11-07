from datetime import datetime


def create_event(
    event_type,
    description,
    source,
    data=None
):

    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "description": description,
        "source": source
    }

    if data is not None:
        event["data"] = data

    return event


def build_url_timeline(
    url,
    url_data,
    dns_data,
    ip_data,
    redirect_data,
    http_data,
    ioc_data,
    correlation_data,
    risk_data
):

    events = []

    events.append(
        create_event(
            "case_start",
            "URL investigation started.",
            "case_manager",
            {
                "url": url
            }
        )
    )

    events.append(
        create_event(
            "url_analysis",
            "URL analysis completed.",
            "url_analyzer",
            {
                "domain":
                    url_data.get("domain"),
                "ip_address":
                    url_data.get("ip_address"),
                "protocol":
                    url_data.get("protocol")
            }
        )
    )

    if dns_data is not None:

        events.append(
            create_event(
                "dns_analysis",
                "DNS analysis completed.",
                "dns_analyzer",
                {
                    "A":
                        len(
                            dns_data.get(
                                "A",
                                []
                            )
                        ),
                    "AAAA":
                        len(
                            dns_data.get(
                                "AAAA",
                                []
                            )
                        ),
                    "MX":
                        len(
                            dns_data.get(
                                "MX",
                                []
                            )
                        ),
                    "NS":
                        len(
                            dns_data.get(
                                "NS",
                                []
                            )
                        ),
                    "TXT":
                        len(
                            dns_data.get(
                                "TXT",
                                []
                            )
                        )
                }
            )
        )

    if ip_data is not None:

        events.append(
            create_event(
                "ip_analysis",
                "IP intelligence analysis completed.",
                "ip_analyzer",
                {
                    "ip_address":
                        ip_data.get(
                            "ip_address"
                        ),
                    "asn":
                        ip_data.get(
                            "asn"
                        ),
                    "network":
                        ip_data.get(
                            "network"
                        ),
                    "country":
                        ip_data.get(
                            "country"
                        )
                }
            )
        )

    events.append(
        create_event(
            "redirect_analysis",
            "Redirect analysis completed.",
            "redirect_analyzer",
            {
                "redirect_count":
                    redirect_data.get(
                        "redirect_count",
                        0
                    ),
                "final_url":
                    redirect_data.get(
                        "final_url"
                    )
            }
        )
    )

    events.append(
        create_event(
            "http_analysis",
            "HTTP analysis completed.",
            "http_analyzer",
            {
                "status_code":
                    http_data.get(
                        "status_code"
                    ),
                "final_url":
                    http_data.get(
                        "final_url"
                    ),
                "server":
                    http_data.get(
                        "server"
                    )
            }
        )
    )

    events.append(
        create_event(
            "ioc_extraction",
            "IOC extraction completed.",
            "ioc_analyzer",
            {
                "primary_count":
                    ioc_data.get(
                        "summary",
                        {}
                    ).get(
                        "primary_count",
                        0
                    ),
                "supporting_count":
                    ioc_data.get(
                        "summary",
                        {}
                    ).get(
                        "supporting_count",
                        0
                    )
            }
        )
    )

    events.append(
        create_event(
            "correlation",
            "Evidence correlation completed.",
            "correlation_engine",
            {
                "entities":
                    correlation_data.get(
                        "entity_count",
                        0
                    ),
                "relationships":
                    correlation_data.get(
                        "relationship_count",
                        0
                    ),
                "correlation_score":
                    correlation_data.get(
                        "correlation_score",
                        {}
                    )
            }
        )
    )

    events.append(
        create_event(
            "risk_assessment",
            "Risk assessment completed.",
            "risk_engine",
            {
                "risk_score":
                    risk_data.get(
                        "risk_score",
                        0
                    ),
                "risk_level":
                    risk_data.get(
                        "risk_level",
                        "LOW"
                    )
            }
        )
    )

    events.append(
        create_event(
            "case_complete",
            "URL investigation completed.",
            "case_manager"
        )
    )

    return events
