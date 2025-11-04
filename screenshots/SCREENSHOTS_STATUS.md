# Screenshots Captured for Capstone Project Submission

## Completed Screenshots:

1. ✅ **django_server.png** - Django server running (Task 2)
2. ✅ **about_us.png** - About Us page (Task 3)
3. ✅ **contact_us.png** - Contact Us page (Task 4)
4. ✅ **login.png** - Login page (Task 5)
5. ✅ **logout_alert.png** - Logout alert (Task 6)
6. ✅ **sign-up.png** - Sign-Up page (Task 7)
7. ⚠️ **express_all_dealers.png** - Express endpoint (Task 9) - Connection refused (backend not running)
8. ⚠️ **express_dealer_details.png** - Express endpoint (Task 10) - Connection refused (backend not running)
9. ⚠️ **express_dealer_reviews.png** - Express endpoint (Task 8) - Connection refused (backend not running)
10. ⚠️ **express_dealers_kansas.png** - Express endpoint (Task 11) - Connection refused (backend not running)
11. ✅ **admin_login.png** - Admin login page (Task 12)
12. ✅ **admin_logged_in.png** - Admin logged in dashboard (Task 12)
13. ✅ **admin_logged_out.png** - Admin logged out (Task 13)
14. ✅ **cars.png** - Car makes page in admin (Task 14)
15. ✅ **car_models.png** - Car models page in admin (Task 15)
16. ⚠️ **sentiment_analyzer.png** - Sentiment analyzer (Task 16) - Connection refused (service not running)
17. ✅ **get_dealers.png** - Dealers page before login (Task 17)
18. ✅ **get_dealers_loggedin.png** - Dealers page after login (Task 18)
19. ✅ **dealers_filtered_state.png** - Dealers filtered by state (Task 19)
20. ⚠️ **dealer_details_reviews.png** - Dealer details with reviews (Task 20) - Empty page (backend not running)
21. ✅ **add_review_before_submit.png** - Add review form filled (Task 21)
22. ⚠️ **added_review.png** - Review added confirmation (Task 22) - May need backend

## Summary:

### Fully Completed (18 screenshots):
- Django static pages (Tasks 2-7)
- Admin pages (Tasks 12-15)
- Dealers pages (Tasks 17-19)
- Add review form (Task 21)

### Requires Backend Services (4 screenshots):
- Express-Mongo endpoints (Tasks 8-11): Need MongoDB + Express server running
- Sentiment analyzer (Task 16): Need sentiment service running
- Dealer details with reviews (Task 20): Need backend data
- Review submission confirmation (Task 22): May need backend

### Pending (Deployment):
- Task 23: CI/CD GitHub Actions screenshot
- Tasks 24-28: Kubernetes deployment screenshots

## To Complete Remaining Backend Screenshots:

### 1. Start MongoDB:
```bash
cd server/database
docker-compose up -d mongo_db
```

### 2. Start Express Backend:
```bash
cd server/database
node app.js
```

### 3. Start Sentiment Analyzer:
```bash
cd server/djangoapp/microservices
python app.py
```

### 4. Then retake screenshots for:
- Tasks 8-11: Express endpoints
- Task 16: Sentiment analyzer
- Tasks 20, 22: Dealer details and review submission

## Notes:

- All Django application screenshots have been captured successfully
- Backend services screenshots require MongoDB and Express to be running
- Deployment screenshots require Kubernetes setup
- All screenshots are saved in `extra/screenshots/` directory
