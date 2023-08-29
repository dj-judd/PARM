CREATE TYPE "operation_types" AS ENUM (
  'CREATE',
  'UPDATE',
  'DELETE',
  'ARCHIVE'
);

CREATE TYPE "reservation_status" AS ENUM (
  'PENDING',
  'APPROVED',
  'CHECKED_OUT',
  'COMPLETED',
  'CANCELLED',
  'DENIED'
);

CREATE TYPE "code_types" AS ENUM (
  'BARCODE',
  'QR',
  'NFC'
);

CREATE TYPE "property_data_type" AS ENUM (
  'VARCHAR',
  'INTEGER',
  'DECIMAL',
  'REAL',
  'BOOLEAN',
  'TIMESTAMP',
  'DATE'
);

CREATE TYPE "iso_currency_codes" AS ENUM (
  'USD',
  'CAD',
  'MXN'
);

CREATE TYPE "file_categories" AS ENUM (
  'ARCHIVE',
  'DOCUMENT',
  'SPREADSHEET',
  'PRESENTATION',
  'IMAGE',
  'VIDEO',
  'AUDIO'
);

CREATE TYPE "file_types" AS ENUM (
  'JPEG',
  'PNG',
  'GIF',
  'BMP',
  'TIFF',
  'SVG',
  'PDF',
  'DOC',
  'DOCX',
  'TXT',
  'RTF',
  'CSV',
  'XLS',
  'XLSX',
  'PPT',
  'PPTX',
  'ZIP',
  'RAR',
  '7Z',
  'MP3',
  'WAV',
  'MP4',
  'AVI',
  'MKV'
);

CREATE TYPE "email_type" AS ENUM (
  'PERSONAL',
  'WORK',
  'BUSINESS'
);

CREATE TYPE "phone_type" AS ENUM (
  'PERSONAL',
  'WORK',
  'OTHER'
);

CREATE TYPE "attachment_type" AS ENUM (
  'profile_pic',
  'hero_pic',
  'thumbnail',
  'document_cover',
  'avatar',
  'banner',
  'logo',
  'background',
  'icon',
  'miscellaneous'
);

CREATE TYPE "image_size" AS ENUM (
  '0-original',
  '1-xsmall',
  '2-small',
  '3-medium',
  '4-large',
  '5-xlarge',
  '6-mongo'
);

CREATE TYPE "address_type" AS ENUM (
  'RESIDENTIAL',
  'BUSINESS',
  'OTHER'
);

CREATE TYPE "iso_country_codes" AS ENUM (
  'US',
  'CA',
  'MX'
);

CREATE TYPE "timezone_identifiers" AS ENUM (
  'Universal Coordinated Time',
  'America/New_York',
  'America/Chicago',
  'America/Denver',
  'America/Los_Angeles',
  'America/Phoenix',
  'America/Anchorage',
  'America/Juneau',
  'America/Honolulu'
);

CREATE TYPE "timezone_abbreviations" AS ENUM (
  'UTC',
  'EST',
  'CST',
  'MST',
  'PST',
  'AKST',
  'HST'
);

CREATE TYPE "state_codes" AS ENUM (
  'AL',
  'AK',
  'AZ',
  'AR',
  'CA',
  'CO',
  'CT',
  'DE',
  'FL',
  'GA',
  'HI',
  'ID',
  'IL',
  'IN',
  'IA',
  'KS',
  'KY',
  'LA',
  'ME',
  'MD',
  'MA',
  'MI',
  'MN',
  'MS',
  'MO',
  'MT',
  'NE',
  'NV',
  'NH',
  'NJ',
  'NM',
  'NY',
  'NC',
  'ND',
  'OH',
  'OK',
  'OR',
  'PA',
  'RI',
  'SC',
  'SD',
  'TN',
  'TX',
  'UT',
  'VT',
  'VA',
  'WA',
  'WV',
  'WI',
  'WY'
);

CREATE TYPE "state_names" AS ENUM (
  'Alabama',
  'Alaska',
  'Arizona',
  'Arkansas',
  'California',
  'Colorado',
  'Connecticut',
  'Delaware',
  'Florida',
  'Georgia',
  'Hawaii',
  'Idaho',
  'Illinois',
  'Indiana',
  'Iowa',
  'Kansas',
  'Kentucky',
  'Louisiana',
  'Maine',
  'Maryland',
  'Massachusetts',
  'Michigan',
  'Minnesota',
  'Mississippi',
  'Missouri',
  'Montana',
  'Nebraska',
  'Nevada',
  'New Hampshire',
  'New Jersey',
  'New Mexico',
  'New York',
  'North Carolina',
  'North Dakota',
  'Ohio',
  'Oklahoma',
  'Oregon',
  'Pennsylvania',
  'Rhode Island',
  'South Carolina',
  'South Dakota',
  'Tennessee',
  'Texas',
  'Utah',
  'Vermont',
  'Virginia',
  'Washington',
  'West Virginia',
  'Wisconsin',
  'Wyoming'
);

CREATE TABLE "global_settings" (
  "id" varchar(64) PRIMARY KEY NOT NULL,
  "default_currency_id" smallint NOT NULL,
  "time_format_is_24h" bool NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "audit_info_entries" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "operation_type" operation_types NOT NULL,
  "details" text,
  "created_by" int NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT (current_timestamp),
  "last_edited_by" int,
  "last_edited_at" timestamp NOT NULL DEFAULT (current_timestamp),
  "is_archived" bool NOT NULL,
  "archived_at" timestamp
);

CREATE TABLE "reservations" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "reserved_for" int NOT NULL,
  "area_id" int NOT NULL,
  "planned_checkout_time" timestamp,
  "planned_checkin_time" timestamp,
  "checkout_time" timestamp,
  "checkin_time" timestamp,
  "is_indefinite" bool NOT NULL DEFAULT (false),
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "reservation_assets" (
  "reservation_id" int NOT NULL,
  "asset_id" int NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "scan_tags" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "asset_id" int NOT NULL,
  "code_data" varchar NOT NULL,
  "code_type" code_types NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "comments" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "parent_comment_id" int,
  "related_entity_type" varchar NOT NULL,
  "related_entity_id" int NOT NULL,
  "comment" text NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "reactions" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "user_id" int NOT NULL,
  "comment_id" int NOT NULL,
  "reaction_type" varchar NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "categories" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "parent_category_id" int,
  "name" varchar NOT NULL,
  "color_id" int NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "colors" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar NOT NULL,
  "hex_value" CHAR(7) NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "custom_properties" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar NOT NULL,
  "prefix" varchar,
  "suffix" varchar,
  "data_type" property_data_type NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "asset_custom_properties" (
  "asset_id" int NOT NULL,
  "property_id" int NOT NULL,
  "value" property_data_type NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "assets" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "brand_id" smallint NOT NULL,
  "model_number" varchar,
  "model_name" varchar NOT NULL,
  "category_id" int,
  "storage_area_id" int,
  "purchase_date" date,
  "purchase_price_id" int,
  "msrp_id" int,
  "residual_value_id" int,
  "parent_asset_id" int,
  "is_kit_root" bool NOT NULL,
  "is_attachment" bool NOT NULL,
  "serial_number" varchar,
  "inventory_number" int,
  "description" varchar,
  "is_available" bool NOT NULL,
  "online_item_page" varchar,
  "warranty_starts" date,
  "warranty_ends" date,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "brand_file_attachments" (
  "brand_id" int NOT NULL,
  "attachment_id" int NOT NULL,
  "attachment_type" attachment_type NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "brand_email_addresses" (
  "brand_id" int NOT NULL,
  "email_address_id" int NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "brand_phone_numbers" (
  "brand_id" int NOT NULL,
  "phone_numbers_id" int NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "brands" (
  "id" SMALLINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar NOT NULL,
  "website" varchar
);

CREATE TABLE "asset_flags" (
  "asset_id" int NOT NULL,
  "flag_id" int NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "flags" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar NOT NULL,
  "description" varchar,
  "color_id" int NOT NULL,
  "makes_unavailable" bool NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "currencies" (
  "id" SMALLINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar NOT NULL,
  "symbol" varchar NOT NULL,
  "iso_code" varchar NOT NULL,
  "exchange_rate" "decimal(10, 5)" NOT NULL
);

CREATE TABLE "financial_entries" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "currency_id" smallint NOT NULL,
  "amount" "decimal(10, 2)" NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "asset_location_logs" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "asset_id" int NOT NULL,
  "latitude" decimal(9,6),
  "longitude" decimal(9,6),
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "asset_file_attachments" (
  "asset_id" int NOT NULL,
  "attachment_id" int NOT NULL,
  "attachment_type" attachment_type NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "file_attachments" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "file_data" bytea,
  "file_url" varchar,
  "file_type" file_types NOT NULL,
  "file_category" file_categories NOT NULL,
  "image_size" image_size,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "user_email_addresses" (
  "user_id" int NOT NULL,
  "email_address_id" int NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "email_addresses" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "email_adderss" varchar NOT NULL,
  "type" email_type NOT NULL,
  "is_verified" bool NOT NULL,
  "is_primary" bool,
  "is_shared" bool,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "user_phone_numbers" (
  "user_id" int NOT NULL,
  "phone_numbers_id" int NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "phone_numbers" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "user_id" int NOT NULL,
  "phone_type" phone_type NOT NULL,
  "is_cell" bool NOT NULL,
  "country_code" smallint NOT NULL,
  "area_code" smallint NOT NULL,
  "phone_number" smallint NOT NULL,
  "extension" smallint,
  "is_verified" bool NOT NULL,
  "is_primary" bool NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "user_settings" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "currency_id" smallint NOT NULL,
  "time_format_is_24h" bool NOT NULL,
  "is_darkmode" bool NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "users" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "password_hash" varchar NOT NULL,
  "first_name" varchar NOT NULL,
  "middle_name" varchar,
  "last_name" varchar NOT NULL,
  "nickname" varchar,
  "nickname_prefered" bool,
  "user_settings_id" int NOT NULL,
  "last_login" timestamp,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "user_file_attachments" (
  "user_id" int NOT NULL,
  "attachment_id" int NOT NULL,
  "attachment_type" attachment_type NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "user_roles" (
  "user_id" int NOT NULL,
  "role_id" int NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "roles" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar NOT NULL,
  "description" text NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "permissions" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar NOT NULL,
  "description" varchar NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "role_permissions" (
  "role_id" int NOT NULL,
  "permission_id" int NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "areas" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "parent_area_id" int,
  "name" varchar NOT NULL,
  "latitude" decimal(9,6),
  "longitude" decimal(9,6),
  "address_id" int,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "area_file_attachments" (
  "area_id" int NOT NULL,
  "attachment_id" int NOT NULL,
  "attachment_type" attachment_type NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "addresses" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar NOT NULL,
  "type" address_type NOT NULL,
  "street" varchar NOT NULL,
  "city" varchar NOT NULL,
  "state_id" smallint NOT NULL,
  "zip" varchar(10) NOT NULL,
  "country_id" smallint NOT NULL,
  "audit_info_entry_id" int NOT NULL
);

CREATE TABLE "countries" (
  "id" SMALLINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "code" iso_country_codes NOT NULL,
  "intl_phone_code" smallint NOT NULL,
  "name" varchar NOT NULL
);

CREATE TABLE "timezones" (
  "id" int PRIMARY KEY NOT NULL,
  "identifier" timezone_identifiers NOT NULL,
  "abbreviation" timezone_abbreviations NOT NULL,
  "utc_offset_minutes" smallint NOT NULL,
  "has_dst" bool NOT NULL
);

CREATE TABLE "states" (
  "id" SMALLINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "code" state_codes NOT NULL,
  "name" state_names NOT NULL,
  "timezone_id" int NOT NULL,
  "country_id" smallint NOT NULL
);

COMMENT ON COLUMN "global_settings"."id" IS 'Primary key';

COMMENT ON COLUMN "global_settings"."default_currency_id" IS 'Foreign key to default currency';

COMMENT ON COLUMN "global_settings"."time_format_is_24h" IS 'Format of time ("12hr" or "24hr")';

COMMENT ON COLUMN "global_settings"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "audit_info_entries"."id" IS 'Primary key';

COMMENT ON COLUMN "audit_info_entries"."operation_type" IS 'Type of operation performed. Example: CREATE, UPDATE, DELETE, ARCHIVE';

COMMENT ON COLUMN "audit_info_entries"."details" IS 'Extra details about the operation';

COMMENT ON COLUMN "audit_info_entries"."created_by" IS 'Foreign key to user who created the record';

COMMENT ON COLUMN "audit_info_entries"."created_at" IS 'Timestamp of creation';

COMMENT ON COLUMN "audit_info_entries"."last_edited_by" IS 'Foreign key to last user who edited the record';

COMMENT ON COLUMN "audit_info_entries"."last_edited_at" IS 'Timestamp of last edit';

COMMENT ON COLUMN "audit_info_entries"."is_archived" IS 'Whether the record is archived';

COMMENT ON COLUMN "audit_info_entries"."archived_at" IS 'Timestamp of when the record was archived';

COMMENT ON COLUMN "reservations"."id" IS 'Primary key';

COMMENT ON COLUMN "reservations"."reserved_for" IS 'Foreign key to user the reservation is for';

COMMENT ON COLUMN "reservations"."area_id" IS 'Foreign key to area of reservation';

COMMENT ON COLUMN "reservations"."planned_checkout_time" IS 'Planned time to check out';

COMMENT ON COLUMN "reservations"."planned_checkin_time" IS 'Planned time to check in';

COMMENT ON COLUMN "reservations"."checkout_time" IS 'Actual checkout time';

COMMENT ON COLUMN "reservations"."checkin_time" IS 'Actual check-in time';

COMMENT ON COLUMN "reservations"."is_indefinite" IS 'If the reservation is going to be indefinate';

COMMENT ON COLUMN "reservations"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "reservation_assets" IS 'Join Table';

COMMENT ON COLUMN "reservation_assets"."audit_info_entry_id" IS 'Points audit table for history of changes.';

COMMENT ON COLUMN "scan_tags"."code_data" IS 'This will contain the actual code or identifier data';

COMMENT ON COLUMN "scan_tags"."code_type" IS 'Type of the code (e.g., BARCODE, QR, NFC)';

COMMENT ON COLUMN "scan_tags"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "comments"."parent_comment_id" IS 'For Nesting';

COMMENT ON COLUMN "comments"."related_entity_type" IS 'This field will denote the type of entity (asset, reservation, image, asset_flag, etc.)';

COMMENT ON COLUMN "comments"."related_entity_id" IS 'This field will store the ID of the related entity in its respective table';

COMMENT ON COLUMN "comments"."comment" IS 'This is where the comment content goes.';

COMMENT ON COLUMN "comments"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "reactions"."user_id" IS 'The user who gave the reaction.';

COMMENT ON COLUMN "reactions"."comment_id" IS 'Which comment the reaction is for.';

COMMENT ON COLUMN "reactions"."reaction_type" IS 'For standard emoji reactions like "thumb_up", "smile", etc.';

COMMENT ON COLUMN "reactions"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "categories"."parent_category_id" IS 'For Nesting';

COMMENT ON COLUMN "categories"."name" IS 'Color for labels and styling';

COMMENT ON COLUMN "categories"."color_id" IS 'Foreign key to color';

COMMENT ON COLUMN "categories"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "colors"."name" IS 'Name for displaying with the color';

COMMENT ON COLUMN "colors"."hex_value" IS 'Hex value for the color';

COMMENT ON COLUMN "colors"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "custom_properties"."name" IS 'Name of the custom property Ex: Screensize';

COMMENT ON COLUMN "custom_properties"."prefix" IS 'Can"t think of an example, but might as well have it. lol xD';

COMMENT ON COLUMN "custom_properties"."suffix" IS '24in ... in, ", ect';

COMMENT ON COLUMN "custom_properties"."data_type" IS 'integer, string, ect.';

COMMENT ON COLUMN "custom_properties"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "asset_custom_properties" IS 'Join Table';

COMMENT ON COLUMN "asset_custom_properties"."value" IS 'The actual value associated with this asset for the given property';

COMMENT ON COLUMN "asset_custom_properties"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "assets"."id" IS 'Primary key';

COMMENT ON COLUMN "assets"."brand_id" IS 'Foreign key to brand';

COMMENT ON COLUMN "assets"."model_number" IS 'Model number of the asset';

COMMENT ON COLUMN "assets"."model_name" IS 'Model name of the asset';

COMMENT ON COLUMN "assets"."category_id" IS 'Foreign key to category';

COMMENT ON COLUMN "assets"."storage_area_id" IS 'Foreign key to storage area';

COMMENT ON COLUMN "assets"."purchase_date" IS 'Purchase date of the asset';

COMMENT ON COLUMN "assets"."purchase_price_id" IS 'Foreign key to purchase price';

COMMENT ON COLUMN "assets"."msrp_id" IS 'Foreign key to manufacturer"s suggested retail price';

COMMENT ON COLUMN "assets"."residual_value_id" IS 'Foreign key to residual value of the asset';

COMMENT ON COLUMN "assets"."parent_asset_id" IS 'If part of a kit, reference to parent asset';

COMMENT ON COLUMN "assets"."is_kit_root" IS 'Indicates if the asset is the root of a kit';

COMMENT ON COLUMN "assets"."is_attachment" IS 'Indicates if the asset is an attachment';

COMMENT ON COLUMN "assets"."serial_number" IS 'Serial number of the asset';

COMMENT ON COLUMN "assets"."inventory_number" IS 'Inventory number of the asset';

COMMENT ON COLUMN "assets"."description" IS 'Description of the asset';

COMMENT ON COLUMN "assets"."is_available" IS 'Availability status of the asset';

COMMENT ON COLUMN "assets"."online_item_page" IS 'Link to the asset"s online page';

COMMENT ON COLUMN "assets"."warranty_starts" IS 'Start date of warranty for the asset';

COMMENT ON COLUMN "assets"."warranty_ends" IS 'End date of warranty for the asset';

COMMENT ON COLUMN "assets"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "brand_file_attachments" IS 'Join Table';

COMMENT ON COLUMN "brand_file_attachments"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "brand_email_addresses" IS 'Join Table';

COMMENT ON COLUMN "brand_email_addresses"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "brand_phone_numbers" IS 'Join Table';

COMMENT ON COLUMN "brand_phone_numbers"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "brands"."name" IS 'Name of the brand. Ex: Canon, Nikon, BlackMagic';

COMMENT ON COLUMN "brands"."website" IS 'ex: www.blackmagicdesign.com';

COMMENT ON TABLE "asset_flags" IS 'Join Table';

COMMENT ON COLUMN "asset_flags"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "flags"."name" IS 'examples: needs cleaning, needs inspection, broken, missing';

COMMENT ON COLUMN "flags"."color_id" IS 'Foreign key to color';

COMMENT ON COLUMN "flags"."makes_unavailable" IS 'If it"s damaged, it"s not available to reserve';

COMMENT ON COLUMN "flags"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "currencies"."id" IS 'Primary key';

COMMENT ON COLUMN "currencies"."name" IS 'Currency name';

COMMENT ON COLUMN "currencies"."symbol" IS 'Currency symbol';

COMMENT ON COLUMN "currencies"."iso_code" IS 'Currency ISO code';

COMMENT ON COLUMN "currencies"."exchange_rate" IS 'what is the exchange rate down to 5 decimals?';

COMMENT ON COLUMN "financial_entries"."id" IS 'Primary key';

COMMENT ON COLUMN "financial_entries"."currency_id" IS 'Reference to currency';

COMMENT ON COLUMN "financial_entries"."amount" IS 'Monetary amount';

COMMENT ON COLUMN "financial_entries"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "asset_location_logs" IS 'for GEO tracking';

COMMENT ON COLUMN "asset_location_logs"."latitude" IS 'GPS Latitude';

COMMENT ON COLUMN "asset_location_logs"."longitude" IS 'GPS Longitude';

COMMENT ON COLUMN "asset_location_logs"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "asset_file_attachments" IS 'Join Table';

COMMENT ON COLUMN "asset_file_attachments"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "file_attachments"."file_data" IS 'Binary data for the attachment';

COMMENT ON COLUMN "file_attachments"."file_url" IS 'URL for the attachment';

COMMENT ON COLUMN "file_attachments"."file_type" IS 'Type of the attachment (e.g., "image", "pdf", "doc")';

COMMENT ON COLUMN "file_attachments"."file_category" IS 'What kind of file is it? Media, document';

COMMENT ON COLUMN "file_attachments"."image_size" IS 'Size type for images';

COMMENT ON COLUMN "file_attachments"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "user_email_addresses" IS 'Join Table';

COMMENT ON COLUMN "user_email_addresses"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "email_addresses"."type" IS 'Type: work, personal, etc.';

COMMENT ON COLUMN "email_addresses"."is_verified" IS 'Verification Status';

COMMENT ON COLUMN "email_addresses"."is_primary" IS 'Primary Email Address';

COMMENT ON COLUMN "email_addresses"."is_shared" IS 'Like a team email';

COMMENT ON COLUMN "email_addresses"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "user_phone_numbers" IS 'Join Table';

COMMENT ON COLUMN "user_phone_numbers"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "phone_numbers"."id" IS 'Unique Identifier';

COMMENT ON COLUMN "phone_numbers"."user_id" IS 'Reference to User';

COMMENT ON COLUMN "phone_numbers"."phone_type" IS 'Type: mobile, work, home';

COMMENT ON COLUMN "phone_numbers"."is_cell" IS 'Is it a cellphone?';

COMMENT ON COLUMN "phone_numbers"."country_code" IS 'Country Code, e.g., +1';

COMMENT ON COLUMN "phone_numbers"."area_code" IS 'Area Code';

COMMENT ON COLUMN "phone_numbers"."phone_number" IS 'Phone Number';

COMMENT ON COLUMN "phone_numbers"."extension" IS 'Optional Extension';

COMMENT ON COLUMN "phone_numbers"."is_verified" IS 'Verification Status';

COMMENT ON COLUMN "phone_numbers"."is_primary" IS 'Primary Phone Number';

COMMENT ON COLUMN "phone_numbers"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "user_settings"."currency_id" IS 'Foreign key to default currency';

COMMENT ON COLUMN "user_settings"."time_format_is_24h" IS 'Format of time ("12hr" or "24hr")';

COMMENT ON COLUMN "user_settings"."is_darkmode" IS 'Could also, be an enum for different themes?';

COMMENT ON COLUMN "user_settings"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "users"."id" IS 'Primary key';

COMMENT ON COLUMN "users"."password_hash" IS 'Hashed password for user';

COMMENT ON COLUMN "users"."first_name" IS 'First name of the user';

COMMENT ON COLUMN "users"."middle_name" IS 'Middle name of the user';

COMMENT ON COLUMN "users"."last_name" IS 'Last name of the user';

COMMENT ON COLUMN "users"."nickname" IS 'Option nickname of the user';

COMMENT ON COLUMN "users"."nickname_prefered" IS 'Do they prefer to go by their nickname?';

COMMENT ON COLUMN "users"."user_settings_id" IS 'Foreign key to user settings';

COMMENT ON COLUMN "users"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "user_file_attachments" IS 'Join Table';

COMMENT ON COLUMN "user_file_attachments"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "user_roles" IS 'Join Table. Track when a user was assigned a specific role.';

COMMENT ON COLUMN "user_roles"."user_id" IS 'Reference to users';

COMMENT ON COLUMN "user_roles"."role_id" IS 'Reference to roles';

COMMENT ON COLUMN "user_roles"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "roles"."id" IS 'Primary key';

COMMENT ON COLUMN "roles"."name" IS 'Role name';

COMMENT ON COLUMN "roles"."description" IS 'Description of the role';

COMMENT ON COLUMN "roles"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "permissions"."id" IS 'Primary key';

COMMENT ON COLUMN "permissions"."name" IS 'Permission name';

COMMENT ON COLUMN "permissions"."description" IS 'Permission description';

COMMENT ON COLUMN "permissions"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "role_permissions" IS 'Join Table. Track when a role was granted a particular permission.';

COMMENT ON COLUMN "role_permissions"."role_id" IS 'Reference to roles';

COMMENT ON COLUMN "role_permissions"."permission_id" IS 'Reference to permissions';

COMMENT ON COLUMN "role_permissions"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "areas" IS 'This will represent different spatial areas that can contain assets. It can be nested to represent a hierarchy of areas, such as buildings, rooms, shelves, etc.';

COMMENT ON COLUMN "areas"."id" IS 'Primary key';

COMMENT ON COLUMN "areas"."parent_area_id" IS 'For nesting';

COMMENT ON COLUMN "areas"."name" IS 'Area name';

COMMENT ON COLUMN "areas"."latitude" IS 'GPS Latitude, optional';

COMMENT ON COLUMN "areas"."longitude" IS 'GPS Longitude, optional';

COMMENT ON COLUMN "areas"."address_id" IS 'If it has an address, what is it?';

COMMENT ON COLUMN "areas"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON TABLE "area_file_attachments" IS 'Join Table';

COMMENT ON COLUMN "area_file_attachments"."attachment_id" IS 'Changed from image_id';

COMMENT ON COLUMN "area_file_attachments"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "addresses"."audit_info_entry_id" IS 'Foreign key to audit information';

COMMENT ON COLUMN "countries"."code" IS 'Country code, e.g., US, CA, MX';

COMMENT ON COLUMN "countries"."intl_phone_code" IS 'International dialing code, e.g., 011, 052';

COMMENT ON COLUMN "timezones"."identifier" IS 'Full Timezone Identifier';

COMMENT ON COLUMN "timezones"."abbreviation" IS 'Timezone Abbreviation Ex: CST';

COMMENT ON COLUMN "states"."timezone_id" IS 'Reference to the timezone table';

ALTER TABLE "global_settings" ADD FOREIGN KEY ("default_currency_id") REFERENCES "currencies" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "global_settings" ("audit_info_entry_id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("created_by") REFERENCES "users" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("last_edited_by") REFERENCES "users" ("id");

ALTER TABLE "reservations" ADD FOREIGN KEY ("reserved_for") REFERENCES "users" ("id");

ALTER TABLE "reservations" ADD FOREIGN KEY ("area_id") REFERENCES "areas" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "reservations" ("audit_info_entry_id");

ALTER TABLE "reservation_assets" ADD FOREIGN KEY ("reservation_id") REFERENCES "reservations" ("id");

ALTER TABLE "reservation_assets" ADD FOREIGN KEY ("asset_id") REFERENCES "assets" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "reservation_assets" ("audit_info_entry_id");

ALTER TABLE "scan_tags" ADD FOREIGN KEY ("asset_id") REFERENCES "assets" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "scan_tags" ("audit_info_entry_id");

ALTER TABLE "comments" ADD FOREIGN KEY ("parent_comment_id") REFERENCES "comments" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "comments" ("audit_info_entry_id");

ALTER TABLE "reactions" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "reactions" ADD FOREIGN KEY ("comment_id") REFERENCES "comments" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "reactions" ("audit_info_entry_id");

ALTER TABLE "categories" ADD FOREIGN KEY ("parent_category_id") REFERENCES "categories" ("id");

ALTER TABLE "categories" ADD FOREIGN KEY ("color_id") REFERENCES "colors" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "categories" ("audit_info_entry_id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "colors" ("audit_info_entry_id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "custom_properties" ("audit_info_entry_id");

ALTER TABLE "asset_custom_properties" ADD FOREIGN KEY ("asset_id") REFERENCES "assets" ("id");

ALTER TABLE "asset_custom_properties" ADD FOREIGN KEY ("property_id") REFERENCES "custom_properties" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "asset_custom_properties" ("audit_info_entry_id");

ALTER TABLE "assets" ADD FOREIGN KEY ("brand_id") REFERENCES "brands" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("category_id") REFERENCES "categories" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("storage_area_id") REFERENCES "areas" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("purchase_price_id") REFERENCES "financial_entries" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("msrp_id") REFERENCES "financial_entries" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("residual_value_id") REFERENCES "financial_entries" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("parent_asset_id") REFERENCES "assets" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "assets" ("audit_info_entry_id");

ALTER TABLE "brand_file_attachments" ADD FOREIGN KEY ("brand_id") REFERENCES "brands" ("id");

ALTER TABLE "brand_file_attachments" ADD FOREIGN KEY ("attachment_id") REFERENCES "file_attachments" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "brand_file_attachments" ("audit_info_entry_id");

ALTER TABLE "brand_email_addresses" ADD FOREIGN KEY ("brand_id") REFERENCES "brands" ("id");

ALTER TABLE "brand_email_addresses" ADD FOREIGN KEY ("email_address_id") REFERENCES "email_addresses" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "brand_email_addresses" ("audit_info_entry_id");

ALTER TABLE "brand_phone_numbers" ADD FOREIGN KEY ("brand_id") REFERENCES "brands" ("id");

ALTER TABLE "brand_phone_numbers" ADD FOREIGN KEY ("phone_numbers_id") REFERENCES "phone_numbers" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "brand_phone_numbers" ("audit_info_entry_id");

ALTER TABLE "asset_flags" ADD FOREIGN KEY ("asset_id") REFERENCES "assets" ("id");

ALTER TABLE "asset_flags" ADD FOREIGN KEY ("flag_id") REFERENCES "flags" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "asset_flags" ("audit_info_entry_id");

ALTER TABLE "flags" ADD FOREIGN KEY ("color_id") REFERENCES "colors" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "flags" ("audit_info_entry_id");

ALTER TABLE "financial_entries" ADD FOREIGN KEY ("currency_id") REFERENCES "currencies" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "financial_entries" ("audit_info_entry_id");

ALTER TABLE "asset_location_logs" ADD FOREIGN KEY ("asset_id") REFERENCES "assets" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "asset_location_logs" ("audit_info_entry_id");

ALTER TABLE "asset_file_attachments" ADD FOREIGN KEY ("asset_id") REFERENCES "assets" ("id");

ALTER TABLE "asset_file_attachments" ADD FOREIGN KEY ("attachment_id") REFERENCES "file_attachments" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "asset_file_attachments" ("audit_info_entry_id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "file_attachments" ("audit_info_entry_id");

ALTER TABLE "user_email_addresses" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "user_email_addresses" ADD FOREIGN KEY ("email_address_id") REFERENCES "email_addresses" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "user_email_addresses" ("audit_info_entry_id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "email_addresses" ("audit_info_entry_id");

ALTER TABLE "user_phone_numbers" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "user_phone_numbers" ADD FOREIGN KEY ("phone_numbers_id") REFERENCES "phone_numbers" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "user_phone_numbers" ("audit_info_entry_id");

ALTER TABLE "phone_numbers" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "phone_numbers" ("audit_info_entry_id");

ALTER TABLE "user_settings" ADD FOREIGN KEY ("currency_id") REFERENCES "currencies" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "user_settings" ("audit_info_entry_id");

ALTER TABLE "users" ADD FOREIGN KEY ("user_settings_id") REFERENCES "user_settings" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "users" ("audit_info_entry_id");

ALTER TABLE "user_file_attachments" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "user_file_attachments" ADD FOREIGN KEY ("attachment_id") REFERENCES "file_attachments" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "user_file_attachments" ("audit_info_entry_id");

ALTER TABLE "user_roles" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "user_roles" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "user_roles" ("audit_info_entry_id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "roles" ("audit_info_entry_id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "permissions" ("audit_info_entry_id");

ALTER TABLE "role_permissions" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id");

ALTER TABLE "role_permissions" ADD FOREIGN KEY ("permission_id") REFERENCES "permissions" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "role_permissions" ("audit_info_entry_id");

ALTER TABLE "areas" ADD FOREIGN KEY ("parent_area_id") REFERENCES "areas" ("id");

ALTER TABLE "areas" ADD FOREIGN KEY ("address_id") REFERENCES "addresses" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "areas" ("audit_info_entry_id");

ALTER TABLE "area_file_attachments" ADD FOREIGN KEY ("area_id") REFERENCES "areas" ("id");

ALTER TABLE "area_file_attachments" ADD FOREIGN KEY ("attachment_id") REFERENCES "file_attachments" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "area_file_attachments" ("audit_info_entry_id");

ALTER TABLE "addresses" ADD FOREIGN KEY ("state_id") REFERENCES "states" ("id");

ALTER TABLE "addresses" ADD FOREIGN KEY ("country_id") REFERENCES "countries" ("id");

ALTER TABLE "audit_info_entries" ADD FOREIGN KEY ("id") REFERENCES "addresses" ("audit_info_entry_id");

ALTER TABLE "states" ADD FOREIGN KEY ("timezone_id") REFERENCES "timezones" ("id");

ALTER TABLE "states" ADD FOREIGN KEY ("country_id") REFERENCES "countries" ("id");
