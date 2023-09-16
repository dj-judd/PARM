CREATE TYPE "operation_types" AS ENUM (
  'CREATE',
  'UPDATE',
  'DELETE',
  'ARCHIVE'
);

CREATE TYPE "auditable_entity_types" AS ENUM (
  'GLOBAL_SETTINGS',
  'UI_THEME',
  'RESERVATION',
  'RESERVATION_ASSET',
  'ASSET_TAG',
  'COMMENT',
  'REACTION',
  'CATEGORY',
  'COLOR',
  'CUSTOM_PROPERTY',
  'ASSET_CUSTOM_PROPERTY',
  'ASSET',
  'MANUFACTURER',
  'ASSET_FLAG',
  'FLAG',
  'FINANCIAL_ENTRY',
  'ASSET_LOCATION_LOG',
  'FILE_ATTACHMENT',
  'EMAIL_ADDRESS',
  'PHONE_NUMBER',
  'USER_SETTINGS',
  'USER',
  'USER_ROLE',
  'ROLE',
  'PERMISSION',
  'ROLE_PERMISSION',
  'AREA',
  'ADDRESS'
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
  'NFC',
  'BLUETOOTH'
);

CREATE TYPE "commentable_entity_types" AS ENUM (
  'COMMENT',
  'ASSET',
  'RESERVATION',
  'AREA',
  'FLAG'
);

CREATE TYPE "reaction_types" AS ENUM (
  '👍️',
  '🤬',
  '💀'
);

CREATE TYPE "custom_property_data_type" AS ENUM (
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

CREATE TYPE "attachable_entity_types" AS ENUM (
  'ASSET',
  'MANUFACTURER',
  'USER',
  'AREA',
  'FLAG'
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

CREATE TYPE "image_size" AS ENUM (
  '0-original',
  '1-xsmall',
  '2-small',
  '3-medium',
  '4-large',
  '5-xlarge',
  '6-mongo'
);

CREATE TYPE "emailable_entity_types" AS ENUM (
  'USER',
  'MANUFACTURER',
  'AREA'
);

CREATE TYPE "email_type" AS ENUM (
  'PERSONAL',
  'WORK',
  'BUSINESS'
);

CREATE TYPE "phoneable_entity_types" AS ENUM (
  'USER',
  'MANUFACTURER',
  'AREA'
);

CREATE TYPE "phone_owner_types" AS ENUM (
  'USER',
  'COMPANY'
);

CREATE TYPE "phone_type" AS ENUM (
  'PERSONAL',
  'WORK',
  'OTHER'
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
  "deployment_fingerprint" varchar(64) PRIMARY KEY NOT NULL,
  "default_currency_id" smallint NOT NULL
);

CREATE TABLE "audit_entries" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "operation_type" operation_types NOT NULL,
  "auditable_entity_type" auditable_entity_types NOT NULL,
  "related_entity_id" int,
  "related_entity_hash" varchar(64),
  "related_composite_id" int,
  "details" text,
  "created_by" int NOT NULL,
  "created_at" timestamp NOT NULL,
  "last_edited_by" int,
  "last_edited_at" timestamp NOT NULL,
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
  "is_indefinite" bool NOT NULL DEFAULT (false)
);

CREATE TABLE "reservation_assets" (
  "reservation_id" int NOT NULL,
  "asset_id" int NOT NULL
);

CREATE TABLE "asset_tags" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "asset_id" int NOT NULL,
  "code_type" code_types NOT NULL,
  "data" varchar NOT NULL
);

CREATE TABLE "comments" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "parent_comment_id" int,
  "commentable_entity_types" commentable_entity_types NOT NULL,
  "entity_id" int NOT NULL,
  "comment_data" varchar(2048) NOT NULL
);

CREATE TABLE "reactions" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "user_id" int NOT NULL,
  "comment_id" int NOT NULL,
  "reaction_type" reaction_types NOT NULL
);

CREATE TABLE "categories" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "parent_category_id" int,
  "name" varchar(64) NOT NULL,
  "color_id" int NOT NULL
);

CREATE TABLE "colors" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar(64) NOT NULL,
  "hex_value" CHAR(9) NOT NULL
);

CREATE TABLE "custom_properties" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar(64) NOT NULL,
  "prefix" varchar(8),
  "suffix" varchar(8),
  "data_type" custom_property_data_type NOT NULL
);

CREATE TABLE "asset_custom_properties" (
  "asset_id" int NOT NULL,
  "custom_property_id" int NOT NULL,
  "data_value" varchar(512) NOT NULL
);

CREATE TABLE "assets" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "manufacturer_id" smallint NOT NULL,
  "model_number" varchar(64),
  "model_name" varchar(64) NOT NULL,
  "category_id" smallint,
  "storage_area_id" int,
  "purchase_date" date,
  "purchase_price_id" int,
  "msrp_id" int,
  "residual_value_id" int,
  "parent_asset_id" int,
  "is_kit_root" bool NOT NULL,
  "is_attachment" bool NOT NULL,
  "serial_number" varchar(256),
  "inventory_number" smallint NOT NULL,
  "description" varchar(512),
  "is_available" bool NOT NULL,
  "online_item_page" varchar,
  "warranty_starts" date,
  "warranty_ends" date
);

CREATE TABLE "manufacturers" (
  "id" SMALLINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar NOT NULL,
  "manufacturer_area_id" int,
  "website" varchar
);

CREATE TABLE "asset_flags" (
  "asset_id" int NOT NULL,
  "flag_id" int NOT NULL
);

CREATE TABLE "flags" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar NOT NULL,
  "description" varchar,
  "color_id" int NOT NULL,
  "makes_unavailable" bool NOT NULL
);

CREATE TABLE "currencies" (
  "id" SMALLINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar(64) NOT NULL,
  "symbol" varchar(8) NOT NULL,
  "iso_code" iso_currency_codes NOT NULL,
  "exchange_rate" decimal(10,5) NOT NULL
);

CREATE TABLE "financial_entries" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "currency_id" smallint NOT NULL,
  "amount" decimal(10,2) NOT NULL
);

CREATE TABLE "asset_location_logs" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "asset_id" int NOT NULL,
  "latitude" decimal(9,6),
  "longitude" decimal(9,6)
);

CREATE TABLE "file_attachments" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "attachable_entity_type" attachable_entity_types NOT NULL,
  "entity_id" int NOT NULL,
  "file_path" varchar UNIQUE,
  "file_type" file_types NOT NULL,
  "file_category" file_categories NOT NULL,
  "image_size" image_size
);

CREATE TABLE "email_addresses" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "emailable_entity_type" emailable_entity_types NOT NULL,
  "entity_id" int NOT NULL,
  "email_type" email_type NOT NULL,
  "email_address" varchar(64) UNIQUE NOT NULL,
  "is_verified" bool NOT NULL,
  "is_primary" bool,
  "is_shared" bool
);

CREATE TABLE "phone_numbers" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "phoneable_entity_type" phoneable_entity_types NOT NULL,
  "entity_id" int NOT NULL,
  "phone_type" phone_type NOT NULL,
  "is_cell" bool NOT NULL,
  "country_code" smallint NOT NULL,
  "area_code" smallint NOT NULL,
  "phone_number" int NOT NULL,
  "extension" smallint,
  "is_verified" bool NOT NULL,
  "is_primary" bool NOT NULL
);

CREATE TABLE "ui_themes" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar(64) UNIQUE NOT NULL,
  "description" varchar(512) NOT NULL,
  "primary_color_id" int NOT NULL,
  "secondary_color_id" int NOT NULL
);

CREATE TABLE "user_settings" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "currency_id" smallint NOT NULL,
  "time_format_is_24h" bool NOT NULL,
  "ui_theme_id" smallint NOT NULL
);

CREATE TABLE "users" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "password_hash" varchar(64) NOT NULL,
  "first_name" varchar(64) NOT NULL,
  "middle_name" varchar(64),
  "last_name" varchar(64) NOT NULL,
  "nickname" varchar(64),
  "nickname_preferred" bool,
  "user_settings_id" int NOT NULL,
  "last_login" timestamp
);

CREATE TABLE "user_roles" (
  "user_id" int NOT NULL,
  "role_id" int NOT NULL
);

CREATE TABLE "roles" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar(64) UNIQUE NOT NULL,
  "description" varchar(512) NOT NULL
);

CREATE TABLE "permissions" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar(64) UNIQUE NOT NULL,
  "description" varchar(512) NOT NULL
);

CREATE TABLE "role_permissions" (
  "role_id" int NOT NULL,
  "permission_id" int NOT NULL
);

CREATE TABLE "areas" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "parent_area_id" int,
  "name" varchar(64) NOT NULL,
  "latitude" decimal(9,6),
  "longitude" decimal(9,6),
  "address_id" int
);

CREATE TABLE "addresses" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "name" varchar(64) NOT NULL,
  "type" address_type NOT NULL,
  "street" varchar NOT NULL,
  "city" varchar NOT NULL,
  "state_id" smallint NOT NULL,
  "zip" varchar(16) NOT NULL,
  "country_id" smallint NOT NULL
);

CREATE TABLE "countries" (
  "id" SMALLINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
  "code" iso_country_codes NOT NULL,
  "name" varchar(64) NOT NULL,
  "intl_phone_code" smallint NOT NULL
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

CREATE INDEX "idx_audit_entries_related_entity_type" ON "audit_entries" ("auditable_entity_type");

CREATE INDEX "idx_audit_entries_related_entity_id" ON "audit_entries" ("related_entity_id");

CREATE INDEX "idx_audit_entries_related_entity_hash" ON "audit_entries" ("related_entity_hash");

CREATE INDEX "idx_audit_entries_related_composite_id" ON "audit_entries" ("related_composite_id");

CREATE INDEX "idx_audit_entries_related_entity_type_id" ON "audit_entries" ("auditable_entity_type", "related_entity_id");

CREATE INDEX "idx_audit_entries_related_entity_type_composite_id" ON "audit_entries" ("auditable_entity_type", "related_composite_id");

CREATE INDEX "idx_audit_entries_created_at" ON "audit_entries" ("created_at");

CREATE INDEX "idx_reservations_area_id" ON "reservations" ("area_id");

CREATE INDEX "idx_reservations_reserved_for" ON "reservations" ("reserved_for");

CREATE INDEX "idx_reservations_planned_checkout_time" ON "reservations" ("planned_checkout_time");

CREATE INDEX "idx_reservations_planned_checkin_time" ON "reservations" ("planned_checkin_time");

CREATE INDEX "idx_reservation_assets_reservation_id" ON "reservation_assets" ("reservation_id");

CREATE INDEX "idx_reservation_assets_asset_id" ON "reservation_assets" ("asset_id");

CREATE INDEX "idx_reservation_assets_reservation_asset" ON "reservation_assets" ("reservation_id", "asset_id");

CREATE INDEX "idx_asset_tags_asset_id" ON "asset_tags" ("asset_id");

CREATE INDEX "idx_asset_tags_code_type" ON "asset_tags" ("code_type");

CREATE INDEX "idx_asset_tags_asset_id_code_type" ON "asset_tags" ("asset_id", "code_type");

CREATE INDEX "idx_comments_commentable_entity_types" ON "comments" ("commentable_entity_types");

CREATE INDEX "idx_comments_related_entity_id" ON "comments" ("entity_id");

CREATE INDEX "idx_comments_commentable_entity_type_id" ON "comments" ("commentable_entity_types", "entity_id");

CREATE INDEX "idx_comments_parent_comment_id" ON "comments" ("parent_comment_id");

CREATE INDEX "idx_comments_parent_comment_id_id" ON "comments" ("parent_comment_id", "id");

CREATE INDEX "idx_reactions_user_id" ON "reactions" ("user_id");

CREATE INDEX "idx_reactions_comment_id" ON "reactions" ("comment_id");

CREATE INDEX "idx_reactions_user_comment_reaction" ON "reactions" ("user_id", "comment_id", "reaction_type");

CREATE INDEX "idx_categories_parent_category_id" ON "categories" ("parent_category_id");

CREATE INDEX "idx_categories_name" ON "categories" ("name");

CREATE INDEX "idx_categories_parent_category_name" ON "categories" ("parent_category_id", "name");

CREATE INDEX "idx_custom_properties_data_type" ON "custom_properties" ("data_type");

CREATE INDEX "idx_asset_custom_properties_asset_id" ON "asset_custom_properties" ("asset_id");

CREATE INDEX "idx_asset_custom_properties_custom_property_id" ON "asset_custom_properties" ("custom_property_id");

CREATE INDEX "idx_asset_custom_properties_asset_custom_property" ON "asset_custom_properties" ("asset_id", "custom_property_id");

CREATE INDEX "idx_assets_manufacturer_id" ON "assets" ("manufacturer_id");

CREATE INDEX "idx_assets_category_id" ON "assets" ("category_id");

CREATE INDEX "idx_assets_storage_area_id" ON "assets" ("storage_area_id");

CREATE INDEX "idx_assets_parent_asset_id" ON "assets" ("parent_asset_id");

CREATE INDEX "idx_assets_is_kit_root" ON "assets" ("is_kit_root");

CREATE INDEX "idx_assets_is_attachment" ON "assets" ("is_attachment");

CREATE INDEX "idx_assets_is_available" ON "assets" ("is_available");

CREATE INDEX "idx_assets_inventory_number" ON "assets" ("inventory_number");

CREATE INDEX "idx_manufacturers_manufacturer_area_id" ON "manufacturers" ("manufacturer_area_id");

CREATE INDEX "idx_manufacturers_website" ON "manufacturers" ("website");

CREATE INDEX "idx_asset_flags_asset_flag" ON "asset_flags" ("asset_id", "flag_id");

CREATE INDEX "idx_flags_color_id" ON "flags" ("color_id");

CREATE INDEX "idx_flags_makes_unavailable" ON "flags" ("makes_unavailable");

CREATE INDEX "idx_flags_name" ON "flags" ("name");

CREATE INDEX "idx_currencies_name" ON "currencies" ("name");

CREATE INDEX "idx_currencies_symbol" ON "currencies" ("symbol");

CREATE INDEX "idx_currencies_iso_code" ON "currencies" ("iso_code");

CREATE INDEX "idx_financial_entries_currency_id" ON "financial_entries" ("currency_id");

CREATE INDEX "idx_financial_entries_amount" ON "financial_entries" ("amount");

CREATE INDEX "idx_asset_location_logs_asset_id" ON "asset_location_logs" ("asset_id");

CREATE INDEX "idx_asset_location_logs_lat_long" ON "asset_location_logs" ("latitude", "longitude");

CREATE INDEX "idx_file_attachments_attachable_entity_type" ON "file_attachments" ("attachable_entity_type");

CREATE INDEX "idx_file_attachments_related_entity_id" ON "file_attachments" ("entity_id");

CREATE INDEX "idx_file_attachments_attachable_entity_type_id" ON "file_attachments" ("attachable_entity_type", "entity_id");

CREATE INDEX "idx_file_attachments_file_type" ON "file_attachments" ("file_type");

CREATE INDEX "idx_file_attachments_file_category" ON "file_attachments" ("file_category");

CREATE INDEX "idx_email_addresses_email_owner_type" ON "email_addresses" ("emailable_entity_type");

CREATE INDEX "idx_email_addresses_related_owner_id" ON "email_addresses" ("entity_id");

CREATE INDEX "idx_email_addresses_email_owner_type_id" ON "email_addresses" ("email_type", "entity_id");

CREATE INDEX "idx_email_addresses_is_verified" ON "email_addresses" ("is_verified");

CREATE INDEX "idx_email_addresses_email_address" ON "email_addresses" ("email_address");

CREATE INDEX "idx_phone_numbers_phone_owner_type" ON "phone_numbers" ("phone_type");

CREATE INDEX "idx_phone_numbers_related_owner_id" ON "phone_numbers" ("entity_id");

CREATE INDEX "idx_phone_numbers_phone_owner_type_id" ON "phone_numbers" ("phone_type", "entity_id");

CREATE INDEX "idx_phone_numbers_is_verified" ON "phone_numbers" ("is_verified");

CREATE INDEX "idx_phone_numbers_phone_number" ON "phone_numbers" ("phone_number");

CREATE INDEX "idx_ui_themes_primary_color_id" ON "ui_themes" ("primary_color_id");

CREATE INDEX "idx_ui_themes_secondary_color_id" ON "ui_themes" ("secondary_color_id");

CREATE INDEX "idx_user_settings_currency_id" ON "user_settings" ("currency_id");

CREATE INDEX "idx_user_settings_ui_theme_id" ON "user_settings" ("ui_theme_id");

CREATE INDEX "idx_users_last_login" ON "users" ("last_login");

CREATE INDEX "idx_user_roles_user_id" ON "user_roles" ("user_id");

CREATE INDEX "idx_user_roles_role_id" ON "user_roles" ("role_id");

CREATE INDEX "idx_role_permissions_role_id" ON "role_permissions" ("role_id");

CREATE INDEX "idx_role_permissions_permission_id" ON "role_permissions" ("permission_id");

CREATE INDEX "idx_areas_parent_area_id" ON "areas" ("parent_area_id");

CREATE INDEX "idx_areas_name" ON "areas" ("name");

CREATE INDEX "idx_areas_address_id" ON "areas" ("address_id");

CREATE INDEX "idx_addresses_state_id" ON "addresses" ("state_id");

CREATE INDEX "idx_addresses_country_id" ON "addresses" ("country_id");

CREATE INDEX "idx_addresses_type" ON "addresses" ("type");

CREATE INDEX "idx_cidx_countries_codeode" ON "countries" ("code");

CREATE INDEX "idx_countries_intl_phone_code" ON "countries" ("intl_phone_code");

CREATE INDEX "idx_timezones_identifier" ON "timezones" ("identifier");

CREATE INDEX "idx_timezones_abbreviation" ON "timezones" ("abbreviation");

CREATE INDEX "idx_states_timezone_id" ON "states" ("timezone_id");

CREATE INDEX "idx_states_country_id" ON "states" ("country_id");

CREATE INDEX "idx_states_code" ON "states" ("code");

CREATE INDEX "idx_states_name" ON "states" ("name");

COMMENT ON COLUMN "global_settings"."deployment_fingerprint" IS 'Primary key';

COMMENT ON COLUMN "global_settings"."default_currency_id" IS 'Foreign key to default currency';

COMMENT ON COLUMN "audit_entries"."id" IS 'Primary key';

COMMENT ON COLUMN "audit_entries"."operation_type" IS 'Type of operation performed. Example: CREATE, UPDATE, DELETE, ARCHIVE';

COMMENT ON COLUMN "audit_entries"."auditable_entity_type" IS 'Type of related entity';

COMMENT ON COLUMN "audit_entries"."related_entity_id" IS 'ID of the related entity';

COMMENT ON COLUMN "audit_entries"."related_entity_hash" IS 'Field for Hashed IDs';

COMMENT ON COLUMN "audit_entries"."related_composite_id" IS 'ID of a composite key, if applicable';

COMMENT ON COLUMN "audit_entries"."details" IS 'Extra details about the operation';

COMMENT ON COLUMN "audit_entries"."created_by" IS 'Foreign key to user who created the record';

COMMENT ON COLUMN "audit_entries"."created_at" IS 'Timestamp of creation';

COMMENT ON COLUMN "audit_entries"."last_edited_by" IS 'Foreign key to last user who edited the record';

COMMENT ON COLUMN "audit_entries"."last_edited_at" IS 'Timestamp of last edit';

COMMENT ON COLUMN "audit_entries"."is_archived" IS 'Whether the record is archived';

COMMENT ON COLUMN "audit_entries"."archived_at" IS 'Timestamp of when the record was archived';

COMMENT ON COLUMN "reservations"."id" IS 'Primary key';

COMMENT ON COLUMN "reservations"."reserved_for" IS 'Foreign key to user the reservation is for';

COMMENT ON COLUMN "reservations"."area_id" IS 'Foreign key to area of reservation';

COMMENT ON COLUMN "reservations"."planned_checkout_time" IS 'Planned time to check out';

COMMENT ON COLUMN "reservations"."planned_checkin_time" IS 'Planned time to check in';

COMMENT ON COLUMN "reservations"."checkout_time" IS 'Actual checkout time';

COMMENT ON COLUMN "reservations"."checkin_time" IS 'Actual check-in time';

COMMENT ON COLUMN "reservations"."is_indefinite" IS 'If the reservation is going to be indefinate';

COMMENT ON TABLE "reservation_assets" IS 'Join Table';

COMMENT ON COLUMN "asset_tags"."code_type" IS 'Type of the code (e.g., BARCODE, QR, NFC)';

COMMENT ON COLUMN "asset_tags"."data" IS 'This will contain the actual code or identifier data';

COMMENT ON COLUMN "comments"."parent_comment_id" IS 'For Nesting';

COMMENT ON COLUMN "comments"."commentable_entity_types" IS 'This field will denote the type of entity (asset, reservation, image, asset_flag, etc.)';

COMMENT ON COLUMN "comments"."entity_id" IS 'This field will store the ID of the related entity in its respective table';

COMMENT ON COLUMN "comments"."comment_data" IS 'This is where the comment content goes.';

COMMENT ON COLUMN "reactions"."user_id" IS 'The user who gave the reaction.';

COMMENT ON COLUMN "reactions"."comment_id" IS 'Which comment the reaction is for.';

COMMENT ON COLUMN "reactions"."reaction_type" IS 'For standard emoji reactions like "thumb_up", "smile", etc.';

COMMENT ON COLUMN "categories"."parent_category_id" IS 'For Nesting';

COMMENT ON COLUMN "categories"."name" IS 'Name of the category';

COMMENT ON COLUMN "categories"."color_id" IS 'Foreign key to color';

COMMENT ON COLUMN "colors"."name" IS 'Name for displaying with the color';

COMMENT ON COLUMN "colors"."hex_value" IS 'Hex value for the color';

COMMENT ON COLUMN "custom_properties"."name" IS 'Name of the custom property Ex: Screensize';

COMMENT ON COLUMN "custom_properties"."prefix" IS 'Can"t think of an example, but might as well have it. lol xD';

COMMENT ON COLUMN "custom_properties"."suffix" IS '24in ... in, ", ect';

COMMENT ON COLUMN "custom_properties"."data_type" IS 'integer, string, ect.';

COMMENT ON TABLE "asset_custom_properties" IS 'Join Table';

COMMENT ON COLUMN "asset_custom_properties"."data_value" IS 'The actual value associated with this asset for the given property';

COMMENT ON COLUMN "assets"."id" IS 'Primary key';

COMMENT ON COLUMN "assets"."manufacturer_id" IS 'Foreign key to brand';

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

COMMENT ON COLUMN "manufacturers"."name" IS 'Name of the brand. Ex: Canon, Nikon, BlackMagic';

COMMENT ON COLUMN "manufacturers"."manufacturer_area_id" IS 'Foreign key to area id';

COMMENT ON COLUMN "manufacturers"."website" IS 'ex: www.blackmagicdesign.com';

COMMENT ON TABLE "asset_flags" IS 'Join Table';

COMMENT ON COLUMN "flags"."name" IS 'examples: needs cleaning, needs inspection, broken, missing';

COMMENT ON COLUMN "flags"."color_id" IS 'Foreign key to color';

COMMENT ON COLUMN "flags"."makes_unavailable" IS 'If it"s damaged, it"s not available to reserve';

COMMENT ON COLUMN "currencies"."id" IS 'Primary key';

COMMENT ON COLUMN "currencies"."name" IS 'Currency name';

COMMENT ON COLUMN "currencies"."symbol" IS 'Currency symbol';

COMMENT ON COLUMN "currencies"."iso_code" IS 'Currency ISO code';

COMMENT ON COLUMN "currencies"."exchange_rate" IS 'what is the exchange rate down to 5 decimals?';

COMMENT ON COLUMN "financial_entries"."id" IS 'Primary key';

COMMENT ON COLUMN "financial_entries"."currency_id" IS 'Reference to currency';

COMMENT ON COLUMN "financial_entries"."amount" IS 'Monetary amount';

COMMENT ON TABLE "asset_location_logs" IS 'for GEO tracking';

COMMENT ON COLUMN "asset_location_logs"."latitude" IS 'GPS Latitude';

COMMENT ON COLUMN "asset_location_logs"."longitude" IS 'GPS Longitude';

COMMENT ON COLUMN "file_attachments"."file_path" IS 'Filepath for the attachment';

COMMENT ON COLUMN "ui_themes"."name" IS 'Role name';

COMMENT ON COLUMN "ui_themes"."description" IS 'Description of the role';

COMMENT ON COLUMN "user_settings"."currency_id" IS 'Foreign key to default currency';

COMMENT ON COLUMN "user_settings"."time_format_is_24h" IS 'Format of time ("12hr" or "24hr")';

COMMENT ON COLUMN "user_settings"."ui_theme_id" IS 'Foreign key to UI theme';

COMMENT ON COLUMN "users"."id" IS 'Primary key';

COMMENT ON COLUMN "users"."password_hash" IS 'Hashed password for user';

COMMENT ON COLUMN "users"."first_name" IS 'First name of the user';

COMMENT ON COLUMN "users"."middle_name" IS 'Middle name of the user';

COMMENT ON COLUMN "users"."last_name" IS 'Last name of the user';

COMMENT ON COLUMN "users"."nickname" IS 'Option nickname of the user';

COMMENT ON COLUMN "users"."nickname_preferred" IS 'Do they prefer to go by their nickname?';

COMMENT ON COLUMN "users"."user_settings_id" IS 'Foreign key to user settings';

COMMENT ON TABLE "user_roles" IS 'Join Table. Track when a user was assigned a specific role.';

COMMENT ON COLUMN "user_roles"."user_id" IS 'Reference to users';

COMMENT ON COLUMN "user_roles"."role_id" IS 'Reference to roles';

COMMENT ON COLUMN "roles"."id" IS 'Primary key';

COMMENT ON COLUMN "roles"."name" IS 'Role name';

COMMENT ON COLUMN "roles"."description" IS 'Description of the role';

COMMENT ON COLUMN "permissions"."id" IS 'Primary key';

COMMENT ON COLUMN "permissions"."name" IS 'Permission name';

COMMENT ON COLUMN "permissions"."description" IS 'Permission description';

COMMENT ON TABLE "role_permissions" IS 'Join Table. Track when a role was granted a particular permission.';

COMMENT ON COLUMN "role_permissions"."role_id" IS 'Reference to roles';

COMMENT ON COLUMN "role_permissions"."permission_id" IS 'Reference to permissions';

COMMENT ON TABLE "areas" IS 'This will represent different spatial areas that can contain assets. It can be nested to represent a hierarchy of areas, such as buildings, rooms, shelves, etc.';

COMMENT ON COLUMN "areas"."id" IS 'Primary key';

COMMENT ON COLUMN "areas"."parent_area_id" IS 'For nesting';

COMMENT ON COLUMN "areas"."name" IS 'Area name';

COMMENT ON COLUMN "areas"."latitude" IS 'GPS Latitude, optional';

COMMENT ON COLUMN "areas"."longitude" IS 'GPS Longitude, optional';

COMMENT ON COLUMN "areas"."address_id" IS 'If it has an address, what is it?';

COMMENT ON COLUMN "countries"."code" IS 'Country code, e.g., US, CA, MX';

COMMENT ON COLUMN "countries"."intl_phone_code" IS 'International dialing code, e.g., 011, 052';

COMMENT ON COLUMN "timezones"."identifier" IS 'Full Timezone Identifier';

COMMENT ON COLUMN "timezones"."abbreviation" IS 'Timezone Abbreviation Ex: CST';

COMMENT ON COLUMN "states"."timezone_id" IS 'Reference to the timezone table';

ALTER TABLE "global_settings" ADD FOREIGN KEY ("default_currency_id") REFERENCES "currencies" ("id");

ALTER TABLE "audit_entries" ADD FOREIGN KEY ("created_by") REFERENCES "users" ("id");

ALTER TABLE "audit_entries" ADD FOREIGN KEY ("last_edited_by") REFERENCES "users" ("id");

ALTER TABLE "reservations" ADD FOREIGN KEY ("reserved_for") REFERENCES "users" ("id");

ALTER TABLE "reservations" ADD FOREIGN KEY ("area_id") REFERENCES "areas" ("id");

ALTER TABLE "reservation_assets" ADD FOREIGN KEY ("reservation_id") REFERENCES "reservations" ("id");

ALTER TABLE "reservation_assets" ADD FOREIGN KEY ("asset_id") REFERENCES "assets" ("id");

ALTER TABLE "asset_tags" ADD FOREIGN KEY ("asset_id") REFERENCES "assets" ("id");

ALTER TABLE "comments" ADD FOREIGN KEY ("parent_comment_id") REFERENCES "comments" ("id");

ALTER TABLE "reactions" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "reactions" ADD FOREIGN KEY ("comment_id") REFERENCES "comments" ("id");

ALTER TABLE "categories" ADD FOREIGN KEY ("parent_category_id") REFERENCES "categories" ("id");

ALTER TABLE "categories" ADD FOREIGN KEY ("color_id") REFERENCES "colors" ("id");

ALTER TABLE "asset_custom_properties" ADD FOREIGN KEY ("asset_id") REFERENCES "assets" ("id");

ALTER TABLE "asset_custom_properties" ADD FOREIGN KEY ("custom_property_id") REFERENCES "custom_properties" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("manufacturer_id") REFERENCES "manufacturers" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("category_id") REFERENCES "categories" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("storage_area_id") REFERENCES "areas" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("purchase_price_id") REFERENCES "financial_entries" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("msrp_id") REFERENCES "financial_entries" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("residual_value_id") REFERENCES "financial_entries" ("id");

ALTER TABLE "assets" ADD FOREIGN KEY ("parent_asset_id") REFERENCES "assets" ("id");

ALTER TABLE "manufacturers" ADD FOREIGN KEY ("manufacturer_area_id") REFERENCES "areas" ("id");

ALTER TABLE "asset_flags" ADD FOREIGN KEY ("asset_id") REFERENCES "assets" ("id");

ALTER TABLE "asset_flags" ADD FOREIGN KEY ("flag_id") REFERENCES "flags" ("id");

ALTER TABLE "flags" ADD FOREIGN KEY ("color_id") REFERENCES "colors" ("id");

ALTER TABLE "financial_entries" ADD FOREIGN KEY ("currency_id") REFERENCES "currencies" ("id");

ALTER TABLE "asset_location_logs" ADD FOREIGN KEY ("asset_id") REFERENCES "assets" ("id");

ALTER TABLE "ui_themes" ADD FOREIGN KEY ("primary_color_id") REFERENCES "colors" ("id");

ALTER TABLE "ui_themes" ADD FOREIGN KEY ("secondary_color_id") REFERENCES "colors" ("id");

ALTER TABLE "user_settings" ADD FOREIGN KEY ("currency_id") REFERENCES "currencies" ("id");

ALTER TABLE "user_settings" ADD FOREIGN KEY ("ui_theme_id") REFERENCES "ui_themes" ("id");

ALTER TABLE "users" ADD FOREIGN KEY ("user_settings_id") REFERENCES "user_settings" ("id");

ALTER TABLE "user_roles" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "user_roles" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id");

ALTER TABLE "role_permissions" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id");

ALTER TABLE "role_permissions" ADD FOREIGN KEY ("permission_id") REFERENCES "permissions" ("id");

ALTER TABLE "areas" ADD FOREIGN KEY ("parent_area_id") REFERENCES "areas" ("id");

ALTER TABLE "areas" ADD FOREIGN KEY ("address_id") REFERENCES "addresses" ("id");

ALTER TABLE "addresses" ADD FOREIGN KEY ("state_id") REFERENCES "states" ("id");

ALTER TABLE "addresses" ADD FOREIGN KEY ("country_id") REFERENCES "countries" ("id");

ALTER TABLE "states" ADD FOREIGN KEY ("timezone_id") REFERENCES "timezones" ("id");

ALTER TABLE "states" ADD FOREIGN KEY ("country_id") REFERENCES "countries" ("id");