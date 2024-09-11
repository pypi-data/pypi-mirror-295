CREATE TABLE overleaf_templates_general (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    link TEXT NOT NULL UNIQUE,
    author TEXT,
    preview_image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建触发器来更新 updated_at 字段
CREATE TRIGGER update_overleaf_templates_general_modtime
BEFORE UPDATE ON overleaf_templates_general
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- 创建索引
CREATE INDEX idx_overleaf_templates_general_title ON overleaf_templates_general(title);
CREATE INDEX idx_overleaf_templates_general_author ON overleaf_templates_general(author);


CREATE TABLE overleaf_templates_detail (
    id SERIAL PRIMARY KEY,
    link TEXT NOT NULL UNIQUE,
    last_updated TIMESTAMP,
    license TEXT,
    abstract TEXT,
    open_template_link TEXT,
    view_pdf_link TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建触发器来更新 updated_at 字段
CREATE TRIGGER update_overleaf_templates_detail_modtime
BEFORE UPDATE ON overleaf_templates_detail
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
