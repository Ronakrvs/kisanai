-- Row Level Security: users can only see their own data

ALTER TABLE crop_images ENABLE ROW LEVEL SECURITY;
ALTER TABLE fertilizer_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE yield_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- crop_images policies
CREATE POLICY "Users see own images" ON crop_images
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users insert own images" ON crop_images
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- fertilizer_predictions policies
CREATE POLICY "Users see own fertilizer records" ON fertilizer_predictions
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users insert own fertilizer records" ON fertilizer_predictions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- yield_predictions policies
CREATE POLICY "Users see own yield records" ON yield_predictions
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users insert own yield records" ON yield_predictions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- chat_history policies
CREATE POLICY "Users see own chat" ON chat_history
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users insert own chat" ON chat_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);
