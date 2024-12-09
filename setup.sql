-- Step 1: Drop Tables (if needed) - useful if you want to refresh the setup

-- COMMENT OUT THIS LINE IF YOU WANT TO KEEP THE DATA
--DROP TABLE IF EXISTS audits, transactions, shoes, images, queue, users CASCADE;

-- Step 2: Create or replace the function that updates the 'updated' column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 3: Create the 'users' table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    object_state VARCHAR(50) DEFAULT 'Pending',
    properties JSONB DEFAULT '{}'::JSONB,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 4: Create the 'queue' table
CREATE TABLE queue (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    raw_text TEXT NOT NULL,
    active INT DEFAULT 1,
    object_state VARCHAR(50) DEFAULT 'Pending',
    properties JSONB DEFAULT '{}'::JSONB,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 5: Create the 'images' table
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    queue_id INT NOT NULL REFERENCES queue(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    filetype TEXT NOT NULL,
    filesize INT NOT NULL,
    properties JSONB DEFAULT '{}'::JSONB,
    active INT DEFAULT 1,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 6: Create the 'shoes' table
CREATE TABLE shoes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Basic shoe information
    brand VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    gender VARCHAR(50) NOT NULL,
    size NUMERIC(5, 2) NOT NULL,
    width VARCHAR(50) DEFAULT 'M',
    color VARCHAR(255) NOT NULL,
    shoe_type VARCHAR(100) NOT NULL,
    style VARCHAR(100) NOT NULL,

    -- Additional details
    material VARCHAR(255),
    heel_type VARCHAR(100),
    occasion VARCHAR(100),
    condition VARCHAR(50) DEFAULT 'Brand New, in Box' NOT NULL,
    special_features JSONB,

    -- Product information
    upc VARCHAR(20) UNIQUE,
    msrp NUMERIC(10, 2),
    average_ebay_selling_price NUMERIC(10, 2),
    category VARCHAR(255),

    -- Listing information
    photos JSONB,
    description TEXT,
    ebay_listing_id VARCHAR(50) UNIQUE,
    ebay_listing_url VARCHAR(255),
    listing_status VARCHAR(50) DEFAULT 'Not Listed' NOT NULL,
    listing_start_date TIMESTAMP,
    listing_end_date TIMESTAMP,

    -- Sales information
    sale_price NUMERIC(10, 2),
    buyer_username VARCHAR(255),
    payment_status VARCHAR(50) DEFAULT 'Pending' NOT NULL,
    shipping_status VARCHAR(50) DEFAULT 'Not Shipped' NOT NULL,
    shipping_tracking_number VARCHAR(100),

    -- Common fields
    active BOOLEAN DEFAULT TRUE,
    object_state VARCHAR(50) DEFAULT 'Pending',
    properties JSONB DEFAULT '{}'::JSONB,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 7: Create the 'transactions' table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    shoe_id INT NOT NULL REFERENCES shoes(id) ON DELETE CASCADE,
    queue_id INT REFERENCES queue(id) ON DELETE CASCADE,
    listing_id VARCHAR(50) NOT NULL,
    listing_status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 8: Create the 'audits' table
CREATE TABLE audits (
    id SERIAL PRIMARY KEY,
    shoe_id INT NOT NULL REFERENCES shoes(id) ON DELETE CASCADE,
    queue_id INT REFERENCES queue(id) ON DELETE CASCADE,
    action_type VARCHAR(100) NOT NULL,
    actor VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 9: Add triggers to automatically update the 'updated' field
-- Trigger for 'users' table
CREATE TRIGGER set_updated_at_users
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for 'queue' table
CREATE TRIGGER set_updated_at_queue
BEFORE UPDATE ON queue
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for 'images' table
CREATE TRIGGER set_updated_at_images
BEFORE UPDATE ON images
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for 'shoes' table
CREATE TRIGGER set_updated_at_shoes
BEFORE UPDATE ON shoes
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for 'transactions' table
CREATE TRIGGER set_updated_at_transactions
BEFORE UPDATE ON transactions
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Step 10: Insert default data for users
-- Add myself as the first user
INSERT INTO users (email) VALUES ('adge.denkers@gmail.com');

-- Note: The 'audits' table does not have an 'updated' field or trigger since it is meant for historical tracking.
