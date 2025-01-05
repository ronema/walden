// 获取Google Analytics PV数据
function getGAPvCount() {
  // 需要先在Google Cloud Platform创建项目并启用Analytics API
  // 然后获取访问令牌
  const accessToken = 'YOUR_ACCESS_TOKEN'; // 需要用户提供
  const viewId = 'YOUR_VIEW_ID'; // 需要用户提供

  fetch(`https://analyticsreporting.googleapis.com/v4/reports:batchGet`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      reportRequests: [{
        viewId: viewId,
        dateRanges: [{
          startDate: '2024-01-01',
          endDate: 'today'
        }],
        metrics: [{
          expression: 'ga:pageviews'
        }]
      }]
    })
  })
  .then(response => response.json())
  .then(data => {
    const pvCount = data.reports[0].data.totals[0].values[0];
    console.log('Total pageviews:', pvCount);
  })
  .catch(error => {
    console.error('Error fetching PV count:', error);
  });
}

// 页面加载时获取PV统计
document.addEventListener('DOMContentLoaded', function() {
  getGAPvCount();
  
  // 每5分钟更新一次PV统计
  setInterval(getGAPvCount, 5 * 60 * 1000);
});
