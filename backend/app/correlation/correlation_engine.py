class CorrelationEngine:

    def __init__(self):
        self.entities = {}
        self.relationships = []
        self.findings = []

    def add_entity(self, entity_type, value, source=None):
        if value is None:
            return

        value = str(value).strip()

        if not value:
            return

        key = f"{entity_type}:{value}"

        if key not in self.entities:
            self.entities[key] = {
                "type": entity_type,
                "value": value,
                "sources": []
            }

        if source and source not in self.entities[key]["sources"]:
            self.entities[key]["sources"].append(source)

    def add_relationship(
        self,
        source,
        relation,
        target,
        confidence="observed",
        evidence_strength=50
    ):
        if not source or target is None:
            return

        relationship = {
            "source": str(source),
            "relation": str(relation),
            "target": str(target),
            "confidence": confidence,
            "evidence_strength": evidence_strength
        }

        if relationship not in self.relationships:
            self.relationships.append(relationship)

    def add_finding(
        self,
        finding_type,
        severity,
        confidence,
        evidence_strength,
        message,
        evidence=None
    ):
        finding = {
            "type": finding_type,
            "severity": severity,
            "confidence": confidence,
            "evidence_strength": evidence_strength,
            "message": message
        }

        if evidence is not None:
            finding["evidence"] = evidence

        self.findings.append(finding)

    def correlate(
        self,
        url_data=None,
        dns_data=None,
        ip_data=None,
        tls_data=None
    ):
        url_data = url_data or {}
        dns_data = dns_data or {}
        ip_data = ip_data or {}
        tls_data = tls_data or {}

        url = url_data.get("url")
        protocol = url_data.get("protocol")
        domain = url_data.get("domain")
        port = url_data.get("port")
        ip_address = url_data.get("ip_address")

        # ======================================
        # URL
        # ======================================

        self.add_entity("url", url, "url_analyzer")
        self.add_entity("protocol", protocol, "url_analyzer")
        self.add_entity("domain", domain, "url_analyzer")
        self.add_entity("ip", ip_address, "url_analyzer")

        if port:
            self.add_entity("port", port, "url_analyzer")

        if url and domain:
            self.add_relationship(
                url,
                "contains_domain",
                domain,
                "confirmed",
                95
            )

        if url and protocol:
            self.add_relationship(
                url,
                "uses_protocol",
                protocol,
                "confirmed",
                95
            )

        if url and port:
            self.add_relationship(
                url,
                "uses_port",
                port,
                "confirmed",
                95
            )

        # ======================================
        # DNS
        # ======================================

        dns_domain = dns_data.get("domain")

        self.add_entity(
            "domain",
            dns_domain,
            "dns_analyzer"
        )

        for record in dns_data.get("A", []):
            self.add_entity("ip", record, "dns_A")

            self.add_relationship(
                dns_domain,
                "A_record",
                record,
                "confirmed",
                100
            )

        for record in dns_data.get("AAAA", []):
            self.add_entity("ipv6", record, "dns_AAAA")

            self.add_relationship(
                dns_domain,
                "AAAA_record",
                record,
                "confirmed",
                100
            )

        for record in dns_data.get("CNAME", []):
            value = record.rstrip(".")

            self.add_entity(
                "canonical_name",
                value,
                "dns_CNAME"
            )

            self.add_relationship(
                dns_domain,
                "CNAME_record",
                value,
                "confirmed",
                100
            )

        for record in dns_data.get("MX", []):
            self.add_entity(
                "mail_server",
                record,
                "dns_MX"
            )

            self.add_relationship(
                dns_domain,
                "mail_server",
                record,
                "confirmed",
                100
            )

        for record in dns_data.get("NS", []):
            value = record.rstrip(".")

            self.add_entity(
                "name_server",
                value,
                "dns_NS"
            )

            self.add_relationship(
                dns_domain,
                "name_server",
                value,
                "confirmed",
                100
            )

        for record in dns_data.get("TXT", []):
            self.add_entity(
                "txt_record",
                record,
                "dns_TXT"
            )

            self.add_relationship(
                dns_domain,
                "TXT_record",
                record,
                "confirmed",
                100
            )

        # Structured SOA
        soa = (
            dns_data
            .get("structured", {})
            .get("SOA")
        )

        if soa:
            mname = soa.get("mname")
            rname = soa.get("rname")

            if mname:
                self.add_entity(
                    "soa_primary_server",
                    mname,
                    "dns_SOA"
                )

                self.add_relationship(
                    dns_domain,
                    "SOA_primary",
                    mname,
                    "confirmed",
                    100
                )

            if rname:
                self.add_entity(
                    "soa_responsible",
                    rname,
                    "dns_SOA"
                )

                self.add_relationship(
                    dns_domain,
                    "SOA_responsible",
                    rname,
                    "confirmed",
                    95
                )

        # Structured CAA
        for record in (
            dns_data
            .get("structured", {})
            .get("CAA", [])
        ):
            tag = record.get("tag")
            value = record.get("value")

            if tag and value:
                policy = f"{tag}:{value}"

                self.add_entity(
                    "caa_record",
                    policy,
                    "dns_CAA"
                )

                self.add_relationship(
                    dns_domain,
                    "CAA_policy",
                    policy,
                    "confirmed",
                    100
                )

        # DNSSEC
        if dns_data.get(
            "dnssec",
            {}
        ).get("present"):

            self.add_entity(
                "dnssec",
                dns_domain,
                "dnssec"
            )

            self.add_relationship(
                dns_domain,
                "has_dnssec",
                "true",
                "confirmed",
                100
            )

        # ======================================
        # IP INTELLIGENCE
        # ======================================

        analyzed_ip = ip_data.get("ip_address")
        reverse_dns = ip_data.get("reverse_dns")
        asn = ip_data.get("asn")
        organization = ip_data.get("asn_description")
        network = ip_data.get("network")
        country = ip_data.get("country")

        self.add_entity(
            "ip",
            analyzed_ip,
            "ip_analyzer"
        )

        if reverse_dns:
            self.add_entity(
                "hostname",
                reverse_dns,
                "reverse_dns"
            )

            self.add_relationship(
                analyzed_ip,
                "reverse_dns",
                reverse_dns,
                "confirmed",
                100
            )

        asn_value = None

        if asn:
            asn_value = str(asn)

            if not asn_value.upper().startswith("AS"):
                asn_value = "AS" + asn_value

            self.add_entity(
                "asn",
                asn_value,
                "ipwhois"
            )

            self.add_relationship(
                analyzed_ip,
                "belongs_to_asn",
                asn_value,
                "confirmed",
                100
            )

        if organization:
            self.add_entity(
                "organization",
                organization,
                "ipwhois"
            )

            if asn_value:
                self.add_relationship(
                    asn_value,
                    "described_as",
                    organization,
                    "confirmed",
                    90
                )

        if network:
            self.add_entity(
                "network",
                network,
                "ipwhois"
            )

            self.add_relationship(
                analyzed_ip,
                "belongs_to_network",
                network,
                "confirmed",
                100
            )

        if country:
            self.add_entity(
                "country",
                country,
                "ipwhois"
            )

            self.add_relationship(
                analyzed_ip,
                "located_in",
                country,
                "confirmed",
                90
            )

        # ======================================
        # TLS CERTIFICATE
        # ======================================

        certificate = tls_data.get(
            "certificate",
            {}
        )

        tls_version = tls_data.get(
            "tls_version"
        )

        if tls_version:
            self.add_entity(
                "tls_version",
                tls_version,
                "tls_analyzer"
            )

            if url:
                self.add_relationship(
                    url,
                    "uses_tls",
                    tls_version,
                    "confirmed",
                    95
                )

        serial = certificate.get(
            "serial_number"
        )

        if serial:
            self.add_entity(
                "certificate_serial",
                serial,
                "tls_analyzer"
            )

        issuer_parts = certificate.get(
            "issuer",
            []
        )

        issuer_values = []

        for item in issuer_parts:
            value = item.get("value")

            if value:
                issuer_values.append(str(value))

        issuer = " | ".join(issuer_values)

        if issuer:
            self.add_entity(
                "certificate_issuer",
                issuer,
                "tls_analyzer"
            )

            self.add_relationship(
                domain,
                "certificate_issued_by",
                issuer,
                "confirmed",
                95
            )

        subject_parts = certificate.get(
            "subject",
            []
        )

        subject_values = []

        for item in subject_parts:
            value = item.get("value")

            if value:
                subject_values.append(str(value))

        subject = " | ".join(subject_values)

        if subject:
            self.add_entity(
                "certificate_subject",
                subject,
                "tls_analyzer"
            )

            self.add_relationship(
                domain,
                "certificate_subject",
                subject,
                "confirmed",
                95
            )

        # ======================================
        # CERTIFICATE SAN CORRELATION
        # ======================================

        san = certificate.get(
            "san",
            []
        )

        san_match = False

        for item in san:

            san_value = item.get("value")

            if not san_value:
                continue

            san_value = str(
                san_value
            ).lower()

            self.add_entity(
                "certificate_san",
                san_value,
                "tls_analyzer"
            )

            self.add_relationship(
                "certificate",
                "contains_san",
                san_value,
                "confirmed",
                100
            )

            if domain:

                domain_lower = domain.lower()

                if (
                    san_value == domain_lower
                    or (
                        san_value.startswith("*.")
                        and domain_lower.endswith(
                            san_value[1:]
                        )
                    )
                ):
                    san_match = True

                    self.add_finding(
                        "certificate_domain_match",
                        "info",
                        "very_high",
                        100,
                        "Certificate SAN matches the analyzed domain.",
                        {
                            "domain": domain,
                            "san": san_value
                        }
                    )

        if (
            domain
            and san
            and not san_match
        ):

            self.add_finding(
                "certificate_domain_mismatch",
                "warning",
                "high",
                90,
                "Analyzed domain was not found in the certificate SANs.",
                {
                    "domain": domain
                }
            )

        # ======================================
        # CERTIFICATE VALIDITY
        # ======================================

        days_remaining = certificate.get(
            "days_remaining"
        )

        if days_remaining is not None:

            self.add_entity(
                "certificate_validity",
                days_remaining,
                "tls_analyzer"
            )

            self.add_relationship(
                domain,
                "certificate_days_remaining",
                days_remaining,
                "observed",
                90
            )

        # ======================================
        # CROSS-SOURCE DNS/IP MATCH
        # ======================================

        if (
            ip_address
            and ip_address in dns_data.get(
                "A",
                []
            )
        ):

            self.add_relationship(
                domain,
                "resolves_to",
                ip_address,
                "confirmed",
                100
            )

            self.add_finding(
                "cross_source_match",
                "info",
                "high",
                100,
                "URL resolved IP matches DNS A record.",
                {
                    "domain": domain,
                    "ip": ip_address
                }
            )

        elif ip_address:

            self.add_relationship(
                domain,
                "resolves_to",
                ip_address,
                "observed",
                70
            )

            self.add_finding(
                "dns_ip_mismatch",
                "warning",
                "medium",
                70,
                "Resolved IP was not found in the DNS A records.",
                {
                    "resolved_ip": ip_address,
                    "dns_a_records":
                        dns_data.get("A", [])
                }
            )

        if (
            domain
            and dns_domain
            and domain.lower()
            == dns_domain.lower()
        ):

            self.add_finding(
                "cross_source_match",
                "info",
                "high",
                100,
                "URL domain matches DNS analysis domain.",
                {
                    "domain": domain
                }
            )

        # ======================================
        # URL FINDINGS
        # ======================================

        suspicious = url_data.get(
            "suspicious_indicators",
            []
        )

        if suspicious:

            self.add_finding(
                "url_indicators",
                "warning",
                "high",
                90,
                "Suspicious URL indicators detected.",
                suspicious
            )

        # ======================================
        # IP ERRORS
        # ======================================

        if ip_data.get("errors"):

            self.add_finding(
                "ip_errors",
                "info",
                "high",
                90,
                "Some IP intelligence lookups failed.",
                ip_data["errors"]
            )

        return self.get_result()

    def calculate_correlation_score(self):

        if not self.relationships:
            return {
                "score": 0,
                "level": "none"
            }

        total = sum(
            item.get(
                "evidence_strength",
                0
            )
            for item in self.relationships
        )

        maximum = len(
            self.relationships
        ) * 100

        score = round(
            (total / maximum) * 100
        )

        if score >= 90:
            level = "very_high"
        elif score >= 75:
            level = "high"
        elif score >= 50:
            level = "medium"
        elif score >= 25:
            level = "low"
        else:
            level = "very_low"

        return {
            "score": score,
            "level": level
        }

    def get_result(self):

        return {
            "entity_count":
                len(self.entities),

            "relationship_count":
                len(self.relationships),

            "correlation_score":
                self.calculate_correlation_score(),

            "entities":
                list(self.entities.values()),

            "relationships":
                self.relationships,

            "findings":
                self.findings
        }
