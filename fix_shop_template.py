import os

file_path = r'c:\Users\Will\Desktop\Boomerang\django_app\store\templates\store\shop.html'

content = """{% extends 'store/base.html' %}
{% load static %}

{% block title %}Shop - Boomerang Digital Solutions{% endblock %}

{% block content %}
<div class="container py-8">
    <div style="margin-bottom: var(--space-8);">
        <h1>Shop All Products</h1>
        <p style="color: var(--medium-grey);">Showing {{ page_obj.paginator.count|default:0 }} products</p>
    </div>
    
    <div style="display: grid; grid-template-columns: 280px 1fr; gap: var(--space-8);">
        <!-- Filters Sidebar -->
        <aside class="filter-panel">
            <h3 style="margin-bottom: var(--space-6);">Filters</h3>
            
            <form action="{% url 'shop' %}" method="GET">
                <!-- Category Filter -->
                <div class="filter-section">
                    <div class="filter-title">Category</div>
                    {% for category in categories %}
                        <label class="filter-option">
                            {% if current_category == category.slug %}
                                <input type="radio" name="category" value="{{ category.slug }}" checked>
                            {% else %}
                                <input type="radio" name="category" value="{{ category.slug }}">
                            {% endif %}
                            <span>{{ category.name }}</span>
                        </label>
                    {% endfor %}
                </div>
                
                <!-- Brand Filter -->
                <div class="filter-section">
                    <div class="filter-title">Brand</div>
                    {% for brand in brands %}
                        <label class="filter-option">
                             {% if current_brand == brand.slug %}
                                <input type="radio" name="brand" value="{{ brand.slug }}" checked>
                             {% else %}
                                <input type="radio" name="brand" value="{{ brand.slug }}">
                             {% endif %}
                            <span>{{ brand.name }}</span>
                        </label>
                    {% endfor %}
                </div>
                
                <!-- Stock Status Filter -->
                <div class="filter-section">
                    <div class="filter-title">Availability</div>
                    <label class="filter-option">
                        {% if request.GET.stock == 'in_stock' %}
                            <input type="radio" name="stock" value="in_stock" checked>
                        {% else %}
                            <input type="radio" name="stock" value="in_stock">
                        {% endif %}
                        <span>In Stock</span>
                    </label>
                    <label class="filter-option">
                        {% if request.GET.stock == 'pre_order' %}
                            <input type="radio" name="stock" value="pre_order" checked>
                        {% else %}
                            <input type="radio" name="stock" value="pre_order">
                        {% endif %}
                        <span>Pre-Order</span>
                    </label>
                </div>
                
                <!-- Price Range -->
                <div class="filter-section" style="background: var(--off-white); padding: var(--space-4); border-radius: var(--radius-md);">
                    <div class="filter-title" style="margin-bottom: var(--space-2); font-size: var(--text-sm); font-weight: 600;">Price Range (KES)</div>
                    <div class="price-range" style="display: flex; align-items: center; gap: var(--space-2);">
                        <input type="number" name="min_price" class="price-input" placeholder="Min" value="{{ request.GET.min_price|default:'' }}" 
                            style="width: 100%; padding: 8px 12px; border: 1px solid var(--border-grey); border-radius: var(--radius-sm); font-size: var(--text-sm);">
                        <span style="color: var(--medium-grey); font-weight: 500;">-</span>
                        <input type="number" name="max_price" class="price-input" placeholder="Max" value="{{ request.GET.max_price|default:'' }}"
                            style="width: 100%; padding: 8px 12px; border: 1px solid var(--border-grey); border-radius: var(--radius-sm); font-size: var(--text-sm);">
                    </div>
                </div>
                
                <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: var(--space-4);">
                    Apply Filters
                </button>
                <a href="{% url 'shop' %}" class="btn btn-outline" style="width: 100%; margin-top: var(--space-2);">
                    Clear Filters
                </a>
            </form>
        </aside>
        
        <!-- Products Grid -->
        <div>
            <!-- Sort & View Options -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-6);">
                <div style="color: var(--medium-grey);">
                    Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
                </div>
                
                <form action="{% url 'shop' %}" method="GET" style="display: flex; gap: var(--space-2); align-items: center;">
                    <!-- Preserve filters -->
                    {% if current_category %}<input type="hidden" name="category" value="{{ current_category }}">{% endif %}
                    {% if current_brand %}<input type="hidden" name="brand" value="{{ current_brand }}">{% endif %}
                    {% if request.GET.min_price %}<input type="hidden" name="min_price" value="{{ request.GET.min_price }}">{% endif %}
                    {% if request.GET.max_price %}<input type="hidden" name="max_price" value="{{ request.GET.max_price }}">{% endif %}
                    
                    <label for="sort" style="color: var(--dark-grey);">Sort by:</label>
                    <select name="sort" id="sort" class="form-select" style="width: auto;" onchange="this.form.submit()">
                        <option value="newest" {% if request.GET.sort == 'newest' %}selected{% endif %}>Newest First</option>
                        <option value="price_asc" {% if request.GET.sort == 'price_asc' %}selected{% endif %}>Price: Low to High</option>
                        <option value="price_desc" {% if request.GET.sort == 'price_desc' %}selected{% endif %}>Price: High to Low</option>
                        <option value="name" {% if request.GET.sort == 'name' %}selected{% endif %}>Name A-Z</option>
                    </select>
                </form>
            </div>
            
            <!-- Product Grid -->
            {% if page_obj %}
                <div class="grid grid-cols-3 gap-6">
                    {% for product in page_obj %}
                        <a href="{% url 'product_detail' product.slug %}" class="product-card">
                            <div class="product-card-image">
                                {% if product.image %}
                                    <img src="{{ product.image.url }}" alt="{{ product.name }}">
                                {% else %}
                                    <img src="{% static 'store/assets/images/placeholder.png' %}" alt="{{ product.name }}">
                                {% endif %}
                                
                                <span class="product-badge badge-in-stock">
                                    {{ product.get_stock_status_display }}
                                </span>
                            </div>
                            
                            <div class="product-card-content">
                                <!-- Rating stars -->
                                <div class="product-rating">
                                    <div class="product-stars">
                                        ★★★★☆
                                    </div>
                                    <span class="product-review-count">(24)</span>
                                </div>
                                
                                <h3 class="product-name">{{ product.name }}</h3>
                                
                                <!--Specs summary -->
                                {% if product.description %}
                                    <div class="product-brand">{{ product.description|truncatewords:5 }}</div>
                                {% endif %}
                                
                                <div class="product-price">KES {{ product.price }}</div>
                                
                                <button class="product-add-btn">
                                    🛒 Add
                                </button>
                            </div>
                        </a>
                    {% endfor %}
                </div>
                
                <!-- Pagination -->
                {% if page_obj.has_other_pages %}
                    <div style="display: flex; justify-content: center; gap: var(--space-2); margin-top: var(--space-12);">
                        {% if page_obj.has_previous %}
                            <a href="?page={{ page_obj.previous_page_number }}{% if request.GET.urlencode %}&{{ request.GET.urlencode }}{% endif %}" class="btn btn-outline">← Previous</a>
                        {% endif %}
                        
                        {% for i in page_obj.paginator.page_range %}
                            {% if page_obj.number == i %}
                                <span class="btn btn-primary">{{ i }}</span>
                            {% elif i > page_obj.number|add:'-3' and i < page_obj.number|add:'3' %}
                                <a href="?page={{ i }}{% if request.GET.urlencode %}&{{ request.GET.urlencode }}{% endif %}" class="btn btn-outline">{{ i }}</a>
                            {% endif %}
                        {% endfor %}
                        
                        {% if page_obj.has_next %}
                            <a href="?page={{ page_obj.next_page_number }}{% if request.GET.urlencode %}&{{ request.GET.urlencode }}{% endif %}" class="btn btn-outline">Next →</a>
                        {% endif %}
                    </div>
                {% endif %}
            {% else %}
                <div style="text-align: center; padding: var(--space-20); color: var(--medium-grey);">
                    <h3 style="margin-bottom: var(--space-4);">No products found</h3>
                    <p>Try adjusting your filters or browse all products</p>
                    <a href="{% url 'shop' %}" class="btn btn-primary" style="margin-top: var(--space-6);">Clear Filters</a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Successfully wrote {len(content)} bytes to {file_path}")
