-- created with pg_dump -n sunrise -s -h pg-bd-jeremy -x bd > sql/sunrise-setup.sql
--
-- PostgreSQL database dump
--


SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: sunrise; Type: SCHEMA; Schema: -; Owner: sunrise
--

create user sunrise with password 'medxsrZ';
alter user sunrise set search_path =  sunrise, public, fe, cobol, stage;
grant connect on bd to sunrise;
grant usage on bd to sunrise;


CREATE SCHEMA sunrise;

ALTER SCHEMA sunrise OWNER TO sunrise;

SET search_path = sunrise, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = true;

--
-- Name: adjuster; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

SET default_with_oids = false;

--
-- Name: batch_file; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE batch_file (
    batch_file_id integer NOT NULL,
    batch_date date NOT NULL,
    file_name character varying(255) NOT NULL,
    username character varying(255),
    create_date timestamp without time zone DEFAULT now()
);


ALTER TABLE sunrise.batch_file OWNER TO sunrise;

--
-- Name: card_print_log; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE card_print_log (
    group_number character varying(8),
    ssn character varying(11),
    dob date,
    patient_id bigint,
    print_time timestamp without time zone NOT NULL,
    username character varying(25)
);


ALTER TABLE sunrise.card_print_log OWNER TO sunrise;

--
-- Name: client; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE client (
    group_number character varying(255) NOT NULL,
    client_name character varying(255),
    address_1 character varying(255),
    address_2 character varying(255),
    city character varying(255),
    state character(2),
    zip_code character varying(10),
    invoice_processor_code character varying(255) DEFAULT 'PRINT'::character varying,
    contact_name character varying(255),
    memo text,
    billing_name character varying(255),
    invoice_gen_template character varying(255) DEFAULT 'cps'::character varying NOT NULL,
    pl_domain character varying(255) DEFAULT 'go.corporatepharmacy.com'::character varying,
    notify_adjusters boolean DEFAULT true NOT NULL,
    claim_manager_code character varying(255) DEFAULT 'ADJUSTERS'::character varying,
    savings_formula character varying(3) DEFAULT 'SFS'::character varying,
    tin character(9),
    report_code character varying(20),
    group_code character varying(10),
    fl_insurer_code character varying(20),
    contact_phone character varying(16),
    contact_fax character varying(16),
    contact_email character varying(100),
    billing_contact character varying(70),
    billing_phone character varying(16),
    billing_fax character varying(16),
    billing_email character varying(100),
    invoice_multiplier numeric(7,5) DEFAULT 1 NOT NULL,
    print_multiplier_invoice boolean DEFAULT false NOT NULL,
    print_nonmultiplier_invoice boolean DEFAULT false NOT NULL,
    bill_cycle character(1) DEFAULT 'W'::bpchar,
    mo_ship_fee numeric DEFAULT 16.50,
    collections_contact character varying(70),
    collections_phone character varying(16),
    collections_fax character varying(16),
    collections_email character varying(100),
    print_hcfa_1500 boolean DEFAULT false,
    show_awp_on_invoice boolean,
    show_sfs_on_invoice boolean,
    show_copay_on_invoice boolean,
    show_savings_on_invoice boolean,
    ccmsi_savings_percent numeric(4,3),
    send_in_companion_edi boolean DEFAULT false,
    ccmsi_client_number character varying(12),
    uses_formulary boolean,
    formulary character varying(5),
    send_ca_state_reporting boolean DEFAULT false,
    send_fl_state_reporting boolean DEFAULT false,
    send_or_state_reporting boolean DEFAULT false,
    send_tx_state_reporting boolean DEFAULT false,
    send_mg_state_reporting boolean DEFAULT false,
    force_under_state_fee boolean DEFAULT false,
    teamsupport_org_id bigint,
    insurer character varying(255),
    insurer_tin character(9),
    tx_carrier_number character varying(30),
    show_uc_on_invoice boolean DEFAULT false,
    show_all_ingredients_on_invoice boolean DEFAULT false,
    email_adjusters_inv_notification boolean DEFAULT false,
    email_billing_inv_notification boolean DEFAULT false,
    fl_insurer character varying(34),
    tx_insurer character varying(34),
    or_insurer character varying(34),
    ca_insurer character varying(34),
    trans_rebate_amount numeric(10,2),
    nc_insurer character varying(34),
    send_nc_state_reporting boolean,
    auto_apply_trans_rebate boolean DEFAULT false NOT NULL,
    show_cmpd_cost_on_invoice boolean DEFAULT false NOT NULL,
    auto_apply_overpayments boolean DEFAULT false
);


ALTER TABLE sunrise.client OWNER TO sunrise;

--
-- Name: client_note; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE client_note (
    note_id integer NOT NULL,
    group_nbr character varying(8) NOT NULL,
    entry_time timestamp without time zone DEFAULT now(),
    username character varying(50),
    note text
);


ALTER TABLE sunrise.client_note OWNER TO sunrise;

--
-- Name: client_note_note_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE client_note_note_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.client_note_note_id_seq OWNER TO sunrise;

--
-- Name: client_note_note_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE client_note_note_id_seq OWNED BY client_note.note_id;


--
-- Name: client_report_code; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE client_report_code (
    group_number character varying(8) NOT NULL,
    report_code character varying(15) NOT NULL,
    internal boolean DEFAULT false
);


ALTER TABLE sunrise.client_report_code OWNER TO sunrise;

--
-- Name: division_code; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE division_code (
    division_id bigint NOT NULL,
    group_number character varying(8) NOT NULL,
    division_code character varying(15) NOT NULL,
    caption character varying(255) NOT NULL
);


ALTER TABLE sunrise.division_code OWNER TO sunrise;

--
-- Name: division_code_division_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE division_code_division_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.division_code_division_id_seq OWNER TO sunrise;

--
-- Name: division_code_division_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE division_code_division_id_seq OWNED BY division_code.division_id;


--
-- Name: edi_file; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE edi_file (
    edi_file_id integer NOT NULL,
    trans_file_id integer,
    group_number character varying(8),
    create_time timestamp without time zone DEFAULT now(),
    send_time timestamp without time zone,
    payload bytea
);


ALTER TABLE sunrise.edi_file OWNER TO sunrise;

--
-- Name: edi_file_edi_file_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE edi_file_edi_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.edi_file_edi_file_id_seq OWNER TO sunrise;

--
-- Name: edi_file_edi_file_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE edi_file_edi_file_id_seq OWNED BY edi_file.edi_file_id;


--
-- Name: employer; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE employer (
    employer_id integer NOT NULL,
    tin character varying(15),
    group_number character varying(8),
    name character varying(255),
    address_1 character varying(255),
    address_2 character varying(255),
    city character varying(255),
    state character varying(255),
    zip_code character varying(10),
    phone character varying(10),
    fax character varying(10),
    email character varying(255),
    id_number character varying(255),
    policy_number character varying(255)
);


ALTER TABLE sunrise.employer OWNER TO sunrise;

--
-- Name: employer_employer_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE employer_employer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.employer_employer_id_seq OWNER TO sunrise;

--
-- Name: employer_employer_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE employer_employer_id_seq OWNED BY employer.employer_id;


--
-- Name: file_import_history_history_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE file_import_history_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.file_import_history_history_id_seq OWNER TO sunrise;

--
-- Name: file_import_history_history_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE file_import_history_history_id_seq OWNED BY batch_file.batch_file_id;


--
-- Name: fl_provider; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE fl_provider (
    lic_id integer NOT NULL,
    license_number character varying(7),
    last_name character varying(40),
    first_name character varying(40),
    middle_initial character(1),
    mailing_address_line1 character varying(100),
    mailing_address_line2 character varying(100),
    mailing_address_city character varying(100),
    mailing_address_state character(2),
    mailing_address_zip character varying(10),
    area_code character(5),
    phone_number character varying(12)
);


ALTER TABLE sunrise.fl_provider OWNER TO sunrise;

--
-- Name: fl_sr_response; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE fl_sr_response (
    response_file_id integer NOT NULL,
    file_data text,
    file_name character varying(100)
);


ALTER TABLE sunrise.fl_sr_response OWNER TO sunrise;

--
-- Name: fl_sr_response_response_file_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE fl_sr_response_response_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.fl_sr_response_response_file_id_seq OWNER TO sunrise;

--
-- Name: fl_sr_response_response_file_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE fl_sr_response_response_file_id_seq OWNED BY fl_sr_response.response_file_id;


--
-- Name: group_info; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE group_info (
    group_number character varying(8) NOT NULL,
    company_name character varying(255) NOT NULL,
    contact_name character varying(255),
    phone character varying(255),
    address_1 character varying(255),
    address_2 character varying(255),
    address_3 character varying(255),
    city character varying(255),
    state character(2),
    zip_code character varying(10),
    email character varying(255),
    authorization_form_type character varying(255),
    authform_header character varying(100),
    reports_menu_flag boolean,
    billing_menu_flag boolean,
    dme_referral_flag boolean,
    rx_history_flag boolean,
    employer_manage_flag boolean,
    expiration_date_required_flag boolean,
    dme_referral_email character varying(255),
    benefit_cap_flag boolean,
    claim_number_regex character varying(255),
    claim_number_error_msg character varying(255),
    data_ref_1_caption character varying(100),
    data_ref_2_caption character varying(100),
    invoice_classes text,
    claim_expiration_flag boolean,
    patient_expiration_flag boolean DEFAULT false,
    email_claim_change_notification_flag boolean DEFAULT false,
    rejection_physician_review_flag boolean DEFAULT false,
    patient_id_regex character varying,
    claim_expiration_requried_flag boolean DEFAULT false,
    cob_flag boolean DEFAULT false,
    patexp_notification_grouping character varying(20) DEFAULT 'multiple'::character varying,
    deactivate_group boolean DEFAULT false,
    patient_exclusion_list_flag boolean DEFAULT false,
    benefit_amt_flag boolean DEFAULT false,
    claim_formulary_flag boolean,
    mtd_benefit_flag boolean DEFAULT false,
    manage_drug_list_flag boolean DEFAULT false,
    auto_apply_overpayments boolean DEFAULT false,
    show_end_user_low_funds boolean DEFAULT false
);


ALTER TABLE sunrise.group_info OWNER TO sunrise;

--
-- Name: invoice; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE invoice (
    invoice_id bigint NOT NULL,
    patient_id bigint,
    group_number character varying(255) NOT NULL,
    batch_date date,
    due_date date,
    total numeric(10,2),
    adjustments numeric(10,2),
    balance numeric(10,2),
    item_count integer,
    memo text,
    manager_id bigint,
    create_date timestamp without time zone DEFAULT now()
);


ALTER TABLE sunrise.invoice OWNER TO sunrise;

--
-- Name: invoice_view; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE invoice_view (
    invoice_id bigint NOT NULL,
    username character varying(255) NOT NULL,
    view_date timestamp without time zone NOT NULL
);


ALTER TABLE sunrise.invoice_view OWNER TO sunrise;

--
-- Name: issue; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE issue (
    issue_id integer NOT NULL,
    creator character varying(255) NOT NULL,
    create_time timestamp without time zone DEFAULT now(),
    update_time timestamp without time zone DEFAULT now(),
    status character varying(15) DEFAULT 'NEW'::character varying,
    product character varying(60),
    category character varying(60),
    description text,
    last_update text,
    requester character varying(50),
    close_date timestamp without time zone,
    closer character varying(50),
    summary character varying(180) NOT NULL
);


ALTER TABLE sunrise.issue OWNER TO sunrise;

--
-- Name: issue_attachment; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE issue_attachment (
    issue_attachment_id integer NOT NULL,
    issue_id integer NOT NULL,
    creator character varying(255),
    create_time timestamp without time zone DEFAULT now(),
    update_time timestamp without time zone DEFAULT now(),
    file_name character varying(255),
    payload bytea
);


ALTER TABLE sunrise.issue_attachment OWNER TO sunrise;

--
-- Name: issue_attachment_issue_attachment_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE issue_attachment_issue_attachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.issue_attachment_issue_attachment_id_seq OWNER TO sunrise;

--
-- Name: issue_attachment_issue_attachment_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE issue_attachment_issue_attachment_id_seq OWNED BY issue_attachment.issue_attachment_id;


--
-- Name: issue_contact; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE issue_contact (
    issue_contact_id integer NOT NULL,
    issue_id integer,
    username character varying(255),
    ctime timestamp without time zone DEFAULT now()
);


ALTER TABLE sunrise.issue_contact OWNER TO sunrise;

--
-- Name: issue_contact_issue_contact_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE issue_contact_issue_contact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.issue_contact_issue_contact_id_seq OWNER TO sunrise;

--
-- Name: issue_contact_issue_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE issue_contact_issue_contact_id_seq OWNED BY issue_contact.issue_contact_id;


--
-- Name: issue_issue_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE issue_issue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.issue_issue_id_seq OWNER TO sunrise;

--
-- Name: issue_issue_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE issue_issue_id_seq OWNED BY issue.issue_id;


--
-- Name: issue_update; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE issue_update (
    issue_update_id integer NOT NULL,
    issue_id integer NOT NULL,
    status character varying(15),
    create_time timestamp without time zone DEFAULT now(),
    update_time timestamp without time zone DEFAULT now(),
    comment text,
    creator character varying(255),
    sender_email character varying(255),
    attachment bytea,
    attachment_file_name character varying(100)
);


ALTER TABLE sunrise.issue_update OWNER TO sunrise;

--
-- Name: issue_update_issue_update_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE issue_update_issue_update_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.issue_update_issue_update_id_seq OWNER TO sunrise;

--
-- Name: issue_update_issue_update_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE issue_update_issue_update_id_seq OWNED BY issue_update.issue_update_id;


--
-- Name: login_log; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE login_log (
    log_id bigint NOT NULL,
    username character varying,
    login_time timestamp without time zone DEFAULT now(),
    user_agent character varying,
    ip_address character varying
);


ALTER TABLE sunrise.login_log OWNER TO sunrise;

--
-- Name: login_log_log_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE login_log_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.login_log_log_id_seq OWNER TO sunrise;

--
-- Name: login_log_log_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE login_log_log_id_seq OWNED BY login_log.log_id;


--
-- Name: managed_group; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE managed_group (
    group_number character varying(8) NOT NULL,
    managed_group_number character varying(8) NOT NULL
);


ALTER TABLE sunrise.managed_group OWNER TO sunrise;

--
-- Name: news_item; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE news_item (
    item_id integer NOT NULL,
    title character varying(255),
    body text,
    publish_date date,
    close_date date,
    create_date timestamp without time zone DEFAULT now(),
    employee_only boolean DEFAULT false,
    written_by character varying(50)
);


ALTER TABLE sunrise.news_item OWNER TO sunrise;

--
-- Name: news_item_item_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE news_item_item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.news_item_item_id_seq OWNER TO sunrise;

--
-- Name: news_item_item_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE news_item_item_id_seq OWNED BY news_item.item_id;


--
-- Name: news_meta; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE news_meta (
    news_class character varying(50)
);


ALTER TABLE sunrise.news_meta OWNER TO sunrise;

--
-- Name: overpayment; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE overpayment (
    overpayment_id bigint NOT NULL,
    trans_id bigint,
    total numeric(10,2),
    balance numeric(10,2),
    entry_date date DEFAULT now(),
    ref_no character varying(20),
    username character varying(50),
    create_date timestamp without time zone DEFAULT now(),
    void_date date
);


ALTER TABLE sunrise.overpayment OWNER TO sunrise;

--
-- Name: overpayment_overpayment_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE overpayment_overpayment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.overpayment_overpayment_id_seq OWNER TO sunrise;

--
-- Name: overpayment_overpayment_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE overpayment_overpayment_id_seq OWNED BY overpayment.overpayment_id;


--
-- Name: physician_review; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE physician_review (
    review_id integer NOT NULL,
    hit_id bigint,
    group_nbr character varying(8) NOT NULL,
    dob date NOT NULL,
    physician_name character varying(60),
    cardholder_nbr character varying(12) NOT NULL,
    review_timestamp timestamp without time zone NOT NULL,
    review text NOT NULL,
    approval character(1) NOT NULL,
    gpi_code character varying(14)
);


ALTER TABLE sunrise.physician_review OWNER TO sunrise;

--
-- Name: physician_review_review_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE physician_review_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.physician_review_review_id_seq OWNER TO sunrise;

--
-- Name: physician_review_review_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE physician_review_review_id_seq OWNED BY physician_review.review_id;


--
-- Name: reversal; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE reversal (
    reversal_id bigint NOT NULL,
    group_number character varying(8) NOT NULL,
    group_auth integer NOT NULL,
    reversal_date date NOT NULL,
    trans_id bigint,
    total numeric(10,2),
    balance numeric(10,2),
    entry_date timestamp without time zone DEFAULT now()
);


ALTER TABLE sunrise.reversal OWNER TO sunrise;

--
-- Name: reversal_reversal_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE reversal_reversal_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.reversal_reversal_id_seq OWNER TO sunrise;

--
-- Name: reversal_reversal_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE reversal_reversal_id_seq OWNED BY reversal.reversal_id;


--
-- Name: settlement; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE settlement (
    settlement_id integer NOT NULL,
    reversal_id bigint,
    overpayment_id bigint,
    create_timestamp timestamp without time zone DEFAULT now(),
    ref_no character varying(50),
    amount numeric(10,2),
    entry_date date DEFAULT now(),
    void_date date,
    username character varying(255)
);


ALTER TABLE sunrise.settlement OWNER TO sunrise;

--
-- Name: settlement_settlement_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE settlement_settlement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.settlement_settlement_id_seq OWNER TO sunrise;

--
-- Name: settlement_settlement_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE settlement_settlement_id_seq OWNED BY settlement.settlement_id;


--
-- Name: state_report_824; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE state_report_824 (
    file_824_id integer NOT NULL,
    file_data text,
    file_name character varying(100)
);


ALTER TABLE sunrise.state_report_824 OWNER TO sunrise;

--
-- Name: state_report_824_file_824_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE state_report_824_file_824_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.state_report_824_file_824_id_seq OWNER TO sunrise;

--
-- Name: state_report_824_file_824_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE state_report_824_file_824_id_seq OWNED BY state_report_824.file_824_id;


--
-- Name: state_report_997; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE state_report_997 (
    file_997_id integer NOT NULL,
    file_data text,
    file_name character varying(100)
);


ALTER TABLE sunrise.state_report_997 OWNER TO sunrise;

--
-- Name: state_report_997_file_997_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE state_report_997_file_997_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.state_report_997_file_997_id_seq OWNER TO sunrise;

--
-- Name: state_report_997_file_997_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE state_report_997_file_997_id_seq OWNED BY state_report_997.file_997_id;


--
-- Name: state_report_entry; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE state_report_entry (
    entry_id bigint NOT NULL,
    file_id integer,
    trans_id bigint NOT NULL,
    control_number bigint,
    ack_code character(1),
    create_date timestamp without time zone DEFAULT now(),
    bill_date date,
    paid_date date,
    response_text text,
    reportzone character(2),
    pending_cancel boolean DEFAULT false,
    cancel_file_id bigint,
    cancel_ack_code character(1),
    bill_id bigint,
    error_msg text,
    response_date date,
    cancel_date date,
    response_desc text[],
    rejection_count integer DEFAULT 0 NOT NULL,
    file_824_id integer,
    file_997_id integer,
    fl_response_file_id integer
);


ALTER TABLE sunrise.state_report_entry OWNER TO sunrise;

--
-- Name: state_report_entry_entry_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE state_report_entry_entry_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.state_report_entry_entry_id_seq OWNER TO sunrise;

--
-- Name: state_report_entry_entry_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE state_report_entry_entry_id_seq OWNED BY state_report_entry.entry_id;


--
-- Name: state_report_file; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE state_report_file (
    file_id integer NOT NULL,
    reportzone character(2) NOT NULL,
    file_name character varying(100) NOT NULL,
    file_type character varying(100) NOT NULL,
    create_date timestamp without time zone DEFAULT now() NOT NULL,
    send_date timestamp without time zone,
    report_date date,
    error_msg text,
    control_number bigint,
    file_data text
);


ALTER TABLE sunrise.state_report_file OWNER TO sunrise;

--
-- Name: state_report_file_file_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE state_report_file_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.state_report_file_file_id_seq OWNER TO sunrise;

--
-- Name: state_report_file_file_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE state_report_file_file_id_seq OWNED BY state_report_file.file_id;


--
-- Name: trans; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE trans (
    trans_id bigint NOT NULL,
    invoice_date date,
    create_date timestamp without time zone DEFAULT now() NOT NULL,
    group_number character varying(8) NOT NULL,
    group_auth bigint,
    invoice_id bigint,
    line_no bigint,
    patient_dob date,
    patient_cardholder_nbr character varying(11) NOT NULL,
    patient_id bigint,
    pharmacy_nabp character varying(7) NOT NULL,
    pharmacy_id bigint,
    doctor_dea_number character varying(9),
    doctor_npi_number character varying(10),
    doctor_id bigint,
    drug_ndc_number character varying(11) NOT NULL,
    drug_id bigint,
    doi date,
    claim_number character varying(255),
    policy_number character varying(255),
    rx_date date NOT NULL,
    rx_number integer,
    date_written date,
    daw character(1),
    quantity numeric(8,3),
    days_supply integer,
    compound_code character varying(255),
    refill_number integer,
    adjuster1_email character varying(50),
    adjuster2_email character varying(50),
    cost_submitted numeric(10,2) NOT NULL,
    sales_tax numeric(11,2) DEFAULT 0.00 NOT NULL,
    usual_customary numeric(10,2) NOT NULL,
    state_fee numeric(10,2) NOT NULL,
    savings numeric(10,2),
    total numeric(11,2),
    balance numeric(11,2),
    awp numeric(10,2),
    tx_type character(2),
    history_id bigint NOT NULL,
    trans_file_id integer,
    sunrise_total numeric(11,2) NOT NULL,
    cps_total numeric(11,2) NOT NULL,
    state_fee_soj smallint
);


ALTER TABLE sunrise.trans OWNER TO sunrise;

--
-- Name: trans_file; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE trans_file (
    trans_file_id integer NOT NULL,
    file_name character varying(50),
    import_timestamp timestamp without time zone DEFAULT now(),
    invoice_date date NOT NULL,
    active boolean DEFAULT false
);


ALTER TABLE sunrise.trans_file OWNER TO sunrise;

--
-- Name: trans_file_trans_file_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE trans_file_trans_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.trans_file_trans_file_id_seq OWNER TO sunrise;

--
-- Name: trans_file_trans_file_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE trans_file_trans_file_id_seq OWNED BY trans_file.trans_file_id;


--
-- Name: trans_log; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE trans_log (
    trans_log_id bigint NOT NULL,
    trans_id integer,
    message text,
    username character varying(255),
    entry_date timestamp without time zone DEFAULT now(),
    facility character varying(255) DEFAULT 'SYSTEM'::character varying NOT NULL,
    flagged boolean DEFAULT false NOT NULL
);


ALTER TABLE sunrise.trans_log OWNER TO sunrise;

--
-- Name: trans_log_trans_log_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE trans_log_trans_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.trans_log_trans_log_id_seq OWNER TO sunrise;

--
-- Name: trans_log_trans_log_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE trans_log_trans_log_id_seq OWNED BY trans_log.trans_log_id;


--
-- Name: trans_payment; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE trans_payment (
    payment_id bigint NOT NULL,
    entry_date date,
    trans_id bigint,
    ref_no character varying(20),
    amount numeric(10,2),
    username character varying(50),
    create_timestamp timestamp without time zone DEFAULT now(),
    overpayment_id bigint,
    reversal_id bigint,
    void_date date
);


ALTER TABLE sunrise.trans_payment OWNER TO sunrise;

--
-- Name: trans_payment_payment_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE trans_payment_payment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.trans_payment_payment_id_seq OWNER TO sunrise;

--
-- Name: trans_payment_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE trans_payment_payment_id_seq OWNED BY trans_payment.payment_id;


--
-- Name: trans_trans_id_seq; Type: SEQUENCE; Schema: sunrise; Owner: sunrise
--

CREATE SEQUENCE trans_trans_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sunrise.trans_trans_id_seq OWNER TO sunrise;

--
-- Name: trans_trans_id_seq; Type: SEQUENCE OWNED BY; Schema: sunrise; Owner: sunrise
--

ALTER SEQUENCE trans_trans_id_seq OWNED BY trans.trans_id;


--
-- Name: user_division_code; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE user_division_code (
    username character varying(255) NOT NULL,
    group_number character varying(255) NOT NULL,
    division_code character varying(255) NOT NULL
);


ALTER TABLE sunrise.user_division_code OWNER TO sunrise;

--
-- Name: user_group_exclusion; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE user_group_exclusion (
    username character varying(50) NOT NULL,
    group_number character varying(8) NOT NULL,
    create_time timestamp without time zone DEFAULT now()
);


ALTER TABLE sunrise.user_group_exclusion OWNER TO sunrise;

--
-- Name: user_info; Type: TABLE; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE TABLE user_info (
    username character varying(50) NOT NULL,
    password character varying(20),
    group_number character varying(8) NOT NULL,
    first_name character varying(255) NOT NULL,
    last_name character varying(255) NOT NULL,
    initials character(2),
    division_code character varying(15),
    email character varying(255),
    internal boolean DEFAULT false,
    admin_flag boolean DEFAULT false,
    sysadmin_flag boolean DEFAULT false,
    add_patient_flag boolean DEFAULT true,
    modify_patient_flag boolean DEFAULT true,
    patient_rx_history_flag boolean DEFAULT true,
    patient_drug_list_flag boolean DEFAULT true,
    daily_transaction_flag boolean,
    group_menu_login_flag boolean,
    internet_tools_flag boolean,
    patient_expirations_flag boolean,
    patient_utilization_flag boolean DEFAULT true,
    reports_flag boolean,
    manage_employer_flag boolean DEFAULT false,
    savings_util_report_flag boolean DEFAULT false,
    last_login timestamp without time zone,
    create_time timestamp without time zone DEFAULT now(),
    modified_time timestamp without time zone,
    start_page character varying(255) DEFAULT 'show_expirations'::character varying NOT NULL,
    print_offset_y integer DEFAULT 0 NOT NULL,
    print_offset_x integer DEFAULT 0 NOT NULL,
    print_card_flag boolean DEFAULT false,
    login_count bigint DEFAULT 0,
    drug_rule_flag boolean DEFAULT false,
    manual_script_entry_flag boolean,
    manage_workqueue_flag boolean DEFAULT false,
    customer_service_flag boolean DEFAULT false,
    doctor_file_maintenance_flag boolean DEFAULT false,
    processor_file_maintenance_flag boolean DEFAULT false,
    accounting_flag boolean DEFAULT false,
    price_rx_flag boolean DEFAULT false,
    developer_flag boolean DEFAULT false,
    profit_dashboard_flag boolean DEFAULT false,
    accman_intel_report_flag boolean DEFAULT false NOT NULL,
    pharmacy_processing_flag boolean DEFAULT true,
    mail_order_alert_flag boolean DEFAULT true,
    rx_intel_report_flag boolean DEFAULT true,
    patient_file_uploads_flag boolean DEFAULT true,
    patient_change_history_flag boolean DEFAULT true,
    patient_referral_services_flag boolean DEFAULT true,
    patient_drug_card_services_flag boolean DEFAULT true,
    patient_physician_contact_flag boolean DEFAULT true,
    notify_fm_update_email character varying(100) DEFAULT NULL::character varying,
    branch_number character varying(40),
    gould_and_lamb_first_fill_flag boolean DEFAULT false,
    phone character varying(12),
    reset_password_hash text,
    reset_password_expiration date,
    active boolean DEFAULT true,
    price_estimator_flag boolean DEFAULT false,
    customer_service_reports_flag boolean DEFAULT false,
    password_expiration_date date,
    view_benefit_amt_flag boolean DEFAULT false,
    admin_group_flag boolean DEFAULT false,
    partner_admin_flag boolean DEFAULT false
);


ALTER TABLE sunrise.user_info OWNER TO sunrise;

--
-- Name: adjuster_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY adjuster ALTER COLUMN adjuster_id SET DEFAULT nextval('adjuster_adjuster_id_seq'::regclass);


--
-- Name: batch_file_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY batch_file ALTER COLUMN batch_file_id SET DEFAULT nextval('file_import_history_history_id_seq'::regclass);


--
-- Name: note_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY client_note ALTER COLUMN note_id SET DEFAULT nextval('client_note_note_id_seq'::regclass);


--
-- Name: division_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY division_code ALTER COLUMN division_id SET DEFAULT nextval('division_code_division_id_seq'::regclass);


--
-- Name: edi_file_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY edi_file ALTER COLUMN edi_file_id SET DEFAULT nextval('edi_file_edi_file_id_seq'::regclass);


--
-- Name: employer_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY employer ALTER COLUMN employer_id SET DEFAULT nextval('employer_employer_id_seq'::regclass);


--
-- Name: response_file_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY fl_sr_response ALTER COLUMN response_file_id SET DEFAULT nextval('fl_sr_response_response_file_id_seq'::regclass);


--
-- Name: issue_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY issue ALTER COLUMN issue_id SET DEFAULT nextval('issue_issue_id_seq'::regclass);


--
-- Name: issue_attachment_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY issue_attachment ALTER COLUMN issue_attachment_id SET DEFAULT nextval('issue_attachment_issue_attachment_id_seq'::regclass);


--
-- Name: issue_contact_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY issue_contact ALTER COLUMN issue_contact_id SET DEFAULT nextval('issue_contact_issue_contact_id_seq'::regclass);


--
-- Name: issue_update_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY issue_update ALTER COLUMN issue_update_id SET DEFAULT nextval('issue_update_issue_update_id_seq'::regclass);


--
-- Name: log_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY login_log ALTER COLUMN log_id SET DEFAULT nextval('login_log_log_id_seq'::regclass);


--
-- Name: item_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY news_item ALTER COLUMN item_id SET DEFAULT nextval('news_item_item_id_seq'::regclass);


--
-- Name: overpayment_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY overpayment ALTER COLUMN overpayment_id SET DEFAULT nextval('overpayment_overpayment_id_seq'::regclass);


--
-- Name: review_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY physician_review ALTER COLUMN review_id SET DEFAULT nextval('physician_review_review_id_seq'::regclass);


--
-- Name: reversal_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY reversal ALTER COLUMN reversal_id SET DEFAULT nextval('reversal_reversal_id_seq'::regclass);


--
-- Name: settlement_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY settlement ALTER COLUMN settlement_id SET DEFAULT nextval('settlement_settlement_id_seq'::regclass);


--
-- Name: file_824_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY state_report_824 ALTER COLUMN file_824_id SET DEFAULT nextval('state_report_824_file_824_id_seq'::regclass);


--
-- Name: file_997_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY state_report_997 ALTER COLUMN file_997_id SET DEFAULT nextval('state_report_997_file_997_id_seq'::regclass);


--
-- Name: entry_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY state_report_entry ALTER COLUMN entry_id SET DEFAULT nextval('state_report_entry_entry_id_seq'::regclass);


--
-- Name: file_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY state_report_file ALTER COLUMN file_id SET DEFAULT nextval('state_report_file_file_id_seq'::regclass);


--
-- Name: trans_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans ALTER COLUMN trans_id SET DEFAULT nextval('trans_trans_id_seq'::regclass);


--
-- Name: trans_file_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans_file ALTER COLUMN trans_file_id SET DEFAULT nextval('trans_file_trans_file_id_seq'::regclass);


--
-- Name: trans_log_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans_log ALTER COLUMN trans_log_id SET DEFAULT nextval('trans_log_trans_log_id_seq'::regclass);


--
-- Name: payment_id; Type: DEFAULT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans_payment ALTER COLUMN payment_id SET DEFAULT nextval('trans_payment_payment_id_seq'::regclass);


--
-- Name: adjuster_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY adjuster
    ADD CONSTRAINT adjuster_pkey PRIMARY KEY (adjuster_id);


--
-- Name: client_note_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY client_note
    ADD CONSTRAINT client_note_pkey PRIMARY KEY (note_id);


--
-- Name: client_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY client
    ADD CONSTRAINT client_pkey PRIMARY KEY (group_number);


--
-- Name: client_report_code_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY client_report_code
    ADD CONSTRAINT client_report_code_pkey PRIMARY KEY (group_number, report_code);


--
-- Name: division_code_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY division_code
    ADD CONSTRAINT division_code_pkey PRIMARY KEY (division_id);


--
-- Name: edi_file_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY edi_file
    ADD CONSTRAINT edi_file_pkey PRIMARY KEY (edi_file_id);


--
-- Name: file_import_history_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY batch_file
    ADD CONSTRAINT file_import_history_pkey PRIMARY KEY (batch_file_id);


--
-- Name: fl_provider_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY fl_provider
    ADD CONSTRAINT fl_provider_pkey PRIMARY KEY (lic_id);


--
-- Name: fl_sr_response_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY fl_sr_response
    ADD CONSTRAINT fl_sr_response_pkey PRIMARY KEY (response_file_id);


--
-- Name: group_info_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY group_info
    ADD CONSTRAINT group_info_pkey PRIMARY KEY (group_number);


--
-- Name: invoice_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY invoice
    ADD CONSTRAINT invoice_pkey PRIMARY KEY (invoice_id);


--
-- Name: invoice_view_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY invoice_view
    ADD CONSTRAINT invoice_view_pkey PRIMARY KEY (invoice_id);


--
-- Name: issue_attachment_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY issue_attachment
    ADD CONSTRAINT issue_attachment_pkey PRIMARY KEY (issue_attachment_id);


--
-- Name: issue_contact_issue_id_key; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY issue_contact
    ADD CONSTRAINT issue_contact_issue_id_key UNIQUE (issue_id, username);


--
-- Name: issue_contact_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY issue_contact
    ADD CONSTRAINT issue_contact_pkey PRIMARY KEY (issue_contact_id);


--
-- Name: issue_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY issue
    ADD CONSTRAINT issue_pkey PRIMARY KEY (issue_id);


--
-- Name: issue_update_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY issue_update
    ADD CONSTRAINT issue_update_pkey PRIMARY KEY (issue_update_id);


--
-- Name: login_log_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY login_log
    ADD CONSTRAINT login_log_pkey PRIMARY KEY (log_id);


--
-- Name: news_item_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY news_item
    ADD CONSTRAINT news_item_pkey PRIMARY KEY (item_id);


--
-- Name: overpayment_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY overpayment
    ADD CONSTRAINT overpayment_pkey PRIMARY KEY (overpayment_id);


--
-- Name: reversal_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY reversal
    ADD CONSTRAINT reversal_pkey PRIMARY KEY (reversal_id);


--
-- Name: settlement_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY settlement
    ADD CONSTRAINT settlement_pkey PRIMARY KEY (settlement_id);


--
-- Name: state_report_824_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY state_report_824
    ADD CONSTRAINT state_report_824_pkey PRIMARY KEY (file_824_id);


--
-- Name: state_report_997_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY state_report_997
    ADD CONSTRAINT state_report_997_pkey PRIMARY KEY (file_997_id);


--
-- Name: state_report_file_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY state_report_file
    ADD CONSTRAINT state_report_file_pkey PRIMARY KEY (file_id);


--
-- Name: trans_file_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY trans_file
    ADD CONSTRAINT trans_file_pkey PRIMARY KEY (trans_file_id);


--
-- Name: trans_payment_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY trans_payment
    ADD CONSTRAINT trans_payment_pkey PRIMARY KEY (payment_id);


--
-- Name: trans_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY trans
    ADD CONSTRAINT trans_pkey PRIMARY KEY (trans_id);


--
-- Name: user_group_exclusion_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY user_group_exclusion
    ADD CONSTRAINT user_group_exclusion_pkey PRIMARY KEY (username, group_number);


--
-- Name: user_info_pkey; Type: CONSTRAINT; Schema: sunrise; Owner: sunrise; Tablespace: 
--

ALTER TABLE ONLY user_info
    ADD CONSTRAINT user_info_pkey PRIMARY KEY (username);


--
-- Name: client_report_code_group_number_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX client_report_code_group_number_idx ON client_report_code USING btree (group_number);


--
-- Name: client_report_code_report_code_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX client_report_code_report_code_idx ON client_report_code USING btree (report_code);


--
-- Name: employer_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE UNIQUE INDEX employer_idx ON employer USING btree (tin, group_number);


--
-- Name: file_824_key; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX file_824_key ON state_report_824 USING btree (file_824_id);


--
-- Name: file_997_key; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX file_997_key ON state_report_997 USING btree (file_997_id);


--
-- Name: invoice_group_number; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX invoice_group_number ON invoice USING btree (group_number);


--
-- Name: invoice_patient_id; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX invoice_patient_id ON invoice USING btree (patient_id);


--
-- Name: issue_attachment_issue_id_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX issue_attachment_issue_id_idx ON issue_attachment USING btree (issue_id);


--
-- Name: issue_status_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX issue_status_idx ON issue USING btree (status);


--
-- Name: issue_update_issue_id_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX issue_update_issue_id_idx ON issue_update USING btree (issue_id);


--
-- Name: sunrise_login_log_username_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX sunrise_login_log_username_idx ON login_log USING btree (username);


--
-- Name: physician_review_gpi_code_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX physician_review_gpi_code_idx ON physician_review USING btree (gpi_code);


--
-- Name: physician_review_hit_id_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX physician_review_hit_id_idx ON physician_review USING btree (hit_id);


--
-- Name: response_file_key; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX response_file_key ON fl_sr_response USING btree (response_file_id);


--
-- Name: state_report_entry_trans_id; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX state_report_entry_trans_id ON state_report_entry USING btree (trans_id);


--
-- Name: trans_doctor_id; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX trans_doctor_id ON trans USING btree (doctor_id);


--
-- Name: trans_history_id_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX trans_history_id_idx ON trans USING btree (history_id);


--
-- Name: trans_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX trans_idx ON trans USING btree (invoice_id);


--
-- Name: trans_idx1; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX trans_idx1 ON trans USING btree (patient_id);


--
-- Name: trans_idx2; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX trans_idx2 ON trans USING btree (doctor_id);


--
-- Name: trans_idx3; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX trans_idx3 ON trans USING btree (drug_id);


--
-- Name: trans_idx4; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX trans_idx4 ON trans USING btree (pharmacy_id);


--
-- Name: trans_log_trans_id; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX trans_log_trans_id ON trans_log USING btree (trans_id);


--
-- Name: user_group_exclude_group_number_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX user_group_exclude_group_number_idx ON user_group_exclusion USING btree (group_number);


--
-- Name: user_group_exclude_username_idx; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE INDEX user_group_exclude_username_idx ON user_group_exclusion USING btree (username);


--
-- Name: user_info_email; Type: INDEX; Schema: sunrise; Owner: sunrise; Tablespace: 
--

CREATE UNIQUE INDEX user_info_email ON user_info USING btree (email);


--
-- Name: card_print_log_patient_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY card_print_log
    ADD CONSTRAINT card_print_log_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: client_report_code_group_number_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY client_report_code
    ADD CONSTRAINT client_report_code_group_number_fkey FOREIGN KEY (group_number) REFERENCES client(group_number) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: edi_file_trans_file_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY edi_file
    ADD CONSTRAINT edi_file_trans_file_id_fkey FOREIGN KEY (trans_file_id) REFERENCES trans_file(trans_file_id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: invoice_fk; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY invoice
    ADD CONSTRAINT invoice_fk FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: invoice_fk1; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--


--
-- Name: issue_attachment_issue_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY issue_attachment
    ADD CONSTRAINT issue_attachment_issue_id_fkey FOREIGN KEY (issue_id) REFERENCES issue(issue_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: issue_contact_issue_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY issue_contact
    ADD CONSTRAINT issue_contact_issue_id_fkey FOREIGN KEY (issue_id) REFERENCES issue(issue_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: issue_contact_username_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY issue_contact
    ADD CONSTRAINT issue_contact_username_fkey FOREIGN KEY (username) REFERENCES user_info(username) ON UPDATE SET NULL ON DELETE SET NULL;


--
-- Name: issue_update_issue_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY issue_update
    ADD CONSTRAINT issue_update_issue_id_fkey FOREIGN KEY (issue_id) REFERENCES issue(issue_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: news_item_written_by_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY news_item
    ADD CONSTRAINT news_item_written_by_fkey FOREIGN KEY (written_by) REFERENCES user_info(username) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: overpayment_trans_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY overpayment
    ADD CONSTRAINT overpayment_trans_id_fkey FOREIGN KEY (trans_id) REFERENCES trans(trans_id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: reversal_trans_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY reversal
    ADD CONSTRAINT reversal_trans_id_fkey FOREIGN KEY (trans_id) REFERENCES trans(trans_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: settlement_overpayment_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY settlement
    ADD CONSTRAINT settlement_overpayment_id_fkey FOREIGN KEY (overpayment_id) REFERENCES overpayment(overpayment_id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: settlement_reversal_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY settlement
    ADD CONSTRAINT settlement_reversal_id_fkey FOREIGN KEY (reversal_id) REFERENCES reversal(reversal_id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: state_report_entry_cancel_file_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY state_report_entry
    ADD CONSTRAINT state_report_entry_cancel_file_id_fkey FOREIGN KEY (cancel_file_id) REFERENCES state_report_file(file_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: state_report_entry_file_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY state_report_entry
    ADD CONSTRAINT state_report_entry_file_id_fkey FOREIGN KEY (file_id) REFERENCES state_report_file(file_id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: state_report_entry_trans_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY state_report_entry
    ADD CONSTRAINT state_report_entry_trans_id_fkey FOREIGN KEY (trans_id) REFERENCES trans(trans_id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: trans_fk; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans
    ADD CONSTRAINT trans_fk FOREIGN KEY (drug_id) REFERENCES public.drug(drug_id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: trans_fk1; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans
    ADD CONSTRAINT trans_fk1 FOREIGN KEY (patient_id) REFERENCES public.patient(patient_id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: trans_fk4; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--


--
-- Name: trans_fk5; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--


--
-- Name: trans_group_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans
    ADD CONSTRAINT trans_group_fkey FOREIGN KEY (group_number) REFERENCES group_info(group_number) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: trans_log_fk; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans_log
    ADD CONSTRAINT trans_log_fk FOREIGN KEY (trans_id) REFERENCES trans(trans_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: trans_payment_overpayment_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans_payment
    ADD CONSTRAINT trans_payment_overpayment_id_fkey FOREIGN KEY (overpayment_id) REFERENCES overpayment(overpayment_id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: trans_payment_reversal_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans_payment
    ADD CONSTRAINT trans_payment_reversal_id_fkey FOREIGN KEY (reversal_id) REFERENCES reversal(reversal_id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: trans_payment_trans_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans_payment
    ADD CONSTRAINT trans_payment_trans_id_fkey FOREIGN KEY (trans_id) REFERENCES trans(trans_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: trans_pharmacy_id_fk; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans
    ADD CONSTRAINT trans_pharmacy_id_fk FOREIGN KEY (pharmacy_id) REFERENCES public.pharmacy(pharmacy_id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: trans_trans_file_id_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY trans
    ADD CONSTRAINT trans_trans_file_id_fkey FOREIGN KEY (trans_file_id) REFERENCES trans_file(trans_file_id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: user_group_exclusion_group_number_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY user_group_exclusion
    ADD CONSTRAINT user_group_exclusion_group_number_fkey FOREIGN KEY (group_number) REFERENCES group_info(group_number) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_group_exclusion_username_fkey; Type: FK CONSTRAINT; Schema: sunrise; Owner: sunrise
--

ALTER TABLE ONLY user_group_exclusion
    ADD CONSTRAINT user_group_exclusion_username_fkey FOREIGN KEY (username) REFERENCES user_info(username) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

grant all on schema sunrise to sunrise;
grant all on all tables in schema sunrise to sunrise;
grant all on all sequences in schema sunrise to sunrise;

grant all on schema cobol to sunrise;
grant all on all tables in schema cobol to sunrise;
grant all on all sequences in schema cobol to sunrise;

grant all on schema public to sunrise;
grant all on all tables in schema public to sunrise;
grant all on all sequences in schema public to sunrise;

grant all on schema fe to sunrise;
grant all on all tables in schema fe to sunrise;
grant all on all sequences in schema fe to sunrise;

grant all on schema stage to sunrise;
grant all on all tables in schema stage to sunrise;
grant all on all sequences in schema stage to sunrise;

insert into sunrise.group_info (group_number, company_name) values ('SUNRISE', 'Sunrise Medical');

insert into sunrise.user_info (username, password, group_number, internal,
                               admin_flag, sysadmin_flag, first_name, last_name)
values ('jeremy', 'python45', 'SUNRISE', true, true, true, 'Jeremy', 'Lowery');

