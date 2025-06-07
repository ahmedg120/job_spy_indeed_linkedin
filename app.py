from flask import Flask, request, jsonify
from flask_cors import CORS
from jobspy import scrape_jobs
import json
from flask import Response
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

@app.route("/scrape_jobs_linkedin", methods=["GET"])
def scrape_linkedin():
    job_title = request.args.get("job_title")
    city = request.args.get("city")
    country = request.args.get("country")

    if not job_title or not city or not country:
        return jsonify({"error": "Please provide job_title, city, and country"}), 400

    location = f"{city}, {country}"

    try:
        jobs_df = scrape_jobs(
            site_name=["linkedin"],
            search_term=job_title,
            location=location,
            results_wanted=20,
            linkedin_fetch_description=True,
            country_indeed=country  # safe to include
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if jobs_df.empty:
        return jsonify([])

    jobs_json = []
    for _, row in jobs_df.iterrows():
        # Handle company_logo
        company_logo = row.get("company_logo")
        if pd.isna(company_logo):
            company_logo = None
            
        # Handle date_posted
        date_posted = row.get("date_posted")
        if pd.isna(date_posted):
            date_posted = None
        else:
            date_posted = date_posted.isoformat()
            
        # Handle job_url
        job_url = row.get("job_url")
        if pd.isna(job_url):
            job_url = None
            
        # Handle title
        title = row.get("title")
        if pd.isna(title):
            title = None
            
        # Handle company
        company = row.get("company")
        if pd.isna(company):
            company = None
            
        # Handle location
        location = row.get("location")
        if pd.isna(location):
            location = None
            
        # Handle job_type
        job_type = row.get("job_type")
        if pd.isna(job_type):
            job_type = None
            
        jobs_json.append({
            "job_url": job_url,
            "title": title,
            "company": company,
            "location": location,
            "date_posted": date_posted,
            "job_type": job_type,
            "company_logo": company_logo
        })

    return jsonify({
        "result": jobs_json,
        "scraped-jobs": len(jobs_json)
    })



@app.route("/scrape_jobs_indeed", methods=["GET"])
def scrape_indeed():
    job_title = request.args.get("job_title")
    city = request.args.get("city")
    country = request.args.get("country")

    if not job_title or not city or not country:
        return jsonify({"error": "Please provide job_title, city, and country"}), 400

    location = f"{city}, {country}"

    try:
        jobs_df = scrape_jobs(
            site_name=["indeed"],
            search_term=job_title,
            location=location,
            country_indeed=country,
            results_wanted=30,
            # Optional filters:
            # job_type='fulltime',  # e.g. 'parttime', 'internship', 'contract'
            # is_remote=False,
            hours_old=None,  # no time limit
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if jobs_df.empty:
        return jsonify([])

    jobs_json = []
    for _, row in jobs_df.iterrows():
        # Handle company_logo
        company_logo = row.get("company_logo")
        if pd.isna(company_logo):
            company_logo = None
            
        # Handle date_posted
        date_posted = row.get("date_posted")
        if pd.isna(date_posted):
            date_posted = None
        else:
            date_posted = date_posted.isoformat()
            
        # Handle job_url
        job_url = row.get("job_url")
        if pd.isna(job_url):
            job_url = None
            
        # Handle title
        title = row.get("title")
        if pd.isna(title):
            title = None
            
        # Handle company
        company = row.get("company")
        if pd.isna(company):
            company = None
            
        # Handle location
        location = row.get("location")
        if pd.isna(location):
            location = None
            
        # Handle job_type
        job_type = row.get("job_type")
        if pd.isna(job_type):
            job_type = None
            
        jobs_json.append({
            "job_url": job_url,
            "title": title,
            "company": company,
            "location": location,
            "date_posted": date_posted,
            "job_type": job_type,
            "company_logo": company_logo
        })

    return jsonify({
        "result": jobs_json,
        "scraped-jobs": len(jobs_json)
    })



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
