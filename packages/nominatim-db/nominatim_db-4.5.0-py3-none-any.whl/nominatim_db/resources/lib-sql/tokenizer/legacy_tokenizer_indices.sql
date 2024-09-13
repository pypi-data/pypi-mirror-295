-- SPDX-License-Identifier: GPL-2.0-only
--
-- This file is part of Nominatim. (https://nominatim.org)
--
-- Copyright (C) 2022 by the Nominatim developer community.
-- For a full list of authors see the git log.

-- Required for details lookup.
CREATE INDEX IF NOT EXISTS idx_word_word_id
  ON word USING BTREE (word_id) {{db.tablespace.search_index}};
